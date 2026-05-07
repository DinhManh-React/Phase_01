import csv
import json
import re
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# Trang danh mục cần cào. Ở đây chỉ lấy thực phẩm chức năng/thuốc,
# tránh cào nhầm voucher, mỹ phẩm, đồ gia dụng...
CATEGORY_URL = "https://chiaki.vn/thuc-pham-chuc-nang"

# Số sản phẩm tối đa muốn lấy trong một lần chạy.
# Muốn lấy nhiều hơn thì tăng số này.
LIMIT = 30

# Header giả lập trình duyệt để website ít chặn request hơn.
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Windows PowerShell đôi khi không in được tiếng Việt nếu dùng encoding mặc định.
# Dòng này ép output của print() sang UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def clean(text):
    # Xóa khoảng trắng thừa, xuống dòng, tab... để dữ liệu gọn hơn.
    # Ví dụ: "  thuốc\n  bổ   gan " -> "thuốc bổ gan"
    return re.sub(r"\s+", " ", text or "").strip()


def soup(url):
    # Gửi request đến URL và lấy HTML về.
    response = requests.get(url, headers=HEADERS, timeout=30)

    # Nếu server trả lỗi như 404, 500... thì dừng chương trình và báo lỗi.
    response.raise_for_status()

    # BeautifulSoup giúp phân tích HTML để có thể dùng select(), get_text()...
    return BeautifulSoup(response.text, "html.parser")


def is_product_url(url):
    # Lấy phần path của URL.
    # Ví dụ: https://chiaki.vn/abc-def?x=1 -> abc-def
    path = urlparse(url).path.strip("/")

    # Một URL sản phẩm trên Chiaki thường có dạng:
    # https://chiaki.vn/ten-san-pham
    # Nếu path có dấu "/" thì thường là trang con/danh mục/tin tức, không lấy.
    return url.startswith("https://chiaki.vn/") and path and "/" not in path


def get_product_links():
    # Mở trang danh mục thực phẩm chức năng.
    page = soup(CATEGORY_URL)
    links = []

    # Tìm các thẻ <a> nằm trong khu vực sản phẩm.
    # Đây là CSS selector:
    # - h3 a[href]: thẻ a có href nằm trong h3
    # - .product a[href]: thẻ a trong class product
    # - .product-item a[href]: thẻ a trong class product-item
    for tag in page.select("h3 a[href], .product a[href], .product-item a[href]"):
        # Chuyển href tương đối thành URL đầy đủ.
        # Ví dụ: /abc -> https://chiaki.vn/abc
        link = urljoin(CATEGORY_URL, tag["href"]).split("#")[0]

        # Chỉ thêm nếu đúng dạng URL sản phẩm và chưa bị trùng.
        if is_product_url(link) and link not in links:
            links.append(link)

        # Đủ số lượng LIMIT thì dừng.
        if len(links) >= LIMIT:
            break

    return links


def get_price(page):
    # Chuyển cả HTML về dạng chuỗi để tìm giá nằm trong dữ liệu JSON nhúng.
    html = str(page)

    # Ưu tiên sale_price vì đây thường là giá bán hiện tại.
    # Regex này tìm dạng: "sale_price": 299000 hoặc "sale_price":"299000"
    match = re.search(r'"sale_price"\s*:\s*"?(\d+)"?', html)

    # Nếu không có sale_price thì lấy price.
    if not match:
        match = re.search(r'"price"\s*:\s*"?(\d+)"?', html)

    if match:
        # Định dạng số 299000 -> 299.000 đ
        return f"{int(match.group(1)):,}".replace(",", ".") + " đ"

    # Trường hợp regex không tìm thấy thì thử lấy từ HTML hiển thị.
    price_tag = page.select_one("#price-show")
    return clean(price_tag.get_text(" ", strip=True)) if price_tag else ""


def get_text_between(lines, start_text, stop_texts):
    # Hàm này lấy đoạn text nằm giữa một dòng bắt đầu và các dòng kết thúc.
    # Dùng để lấy mô tả từ "Mô tả sản phẩm" đến trước "Đánh giá sản phẩm".
    if start_text not in lines:
        return ""

    # Vị trí bắt đầu lấy dữ liệu là dòng ngay sau start_text.
    start = lines.index(start_text) + 1
    end = len(lines)

    # Tìm dòng kết thúc gần nhất.
    for i in range(start, len(lines)):
        if lines[i] in stop_texts:
            end = i
            break

    # Ghép các dòng mô tả thành một chuỗi dài.
    return clean(" ".join(lines[start:end]))


def get_comments(lines):
    # Nếu trang không có khu vực đánh giá thì trả về danh sách rỗng.
    if "Đánh giá sản phẩm" not in lines:
        return []

    # Bắt đầu đọc các dòng sau tiêu đề "Đánh giá sản phẩm".
    start = lines.index("Đánh giá sản phẩm") + 1
    comments = []

    # Chỉ xem khoảng 80 dòng đầu sau phần đánh giá để tránh lấy lan sang khu vực khác.
    for line in lines[start : start + 80]:
        lower = line.lower()

        # Bỏ dòng quá ngắn vì thường là tên người, số sao, label...
        if len(line) < 12:
            continue

        # Bỏ dòng ngày giờ, ví dụ: 14:26, 28/03/2026
        if re.match(r"\d{1,2}:\d{2},\s*\d{2}/\d{2}/\d{4}", line):
            continue

        # Bỏ template Angular như {{product.rating_value}} hoặc tên bị che bằng ***.
        if "{{" in line or "}}" in line or "*" in line:
            continue

        # Bỏ các dòng thuộc form nhập đánh giá, không phải comment thật.
        if any(word in lower for word in ["vui lòng", "email", "số điện thoại", "đánh giá", "hình ảnh"]):
            continue

        # Tránh lưu trùng comment.
        if line not in comments:
            comments.append(line)

    return comments


def scrape_product(url):
    # Mở trang chi tiết sản phẩm.
    page = soup(url)

    # Tách toàn bộ text của trang thành từng dòng sạch.
    # Cách này giúp tìm các mốc như "Mô tả sản phẩm", "Đánh giá sản phẩm".
    lines = [clean(line) for line in page.get_text("\n", strip=True).splitlines()]
    lines = [line for line in lines if line]

    # Tên sản phẩm thường nằm trong #js-product-title hoặc h1.
    name_tag = page.select_one("#js-product-title, h1")

    # Trả về một dict chứa đầy đủ thông tin cần lưu.
    return {
        "url": url,
        "category": "Thực phẩm chức năng / thuốc",
        "name": clean(name_tag.get_text(" ", strip=True)) if name_tag else "",
        "price": get_price(page),
        "description": get_text_between(
            lines,
            "Mô tả sản phẩm",
            ["Đánh giá sản phẩm", "Hỏi đáp", "Sản phẩm tương tự"],
        ),
        "comments": get_comments(lines),
    }


# Lấy danh sách link sản phẩm từ trang danh mục.
links = get_product_links()
products = []

# Vào từng link sản phẩm và cào thông tin chi tiết.
for i, link in enumerate(links, start=1):
    print(f"{i}. Đang cào: {link}")
    products.append(scrape_product(link))

# Lưu dữ liệu dạng JSON.
# JSON giữ được comments dưới dạng list nên dễ dùng lại trong Python.
with open("chiaki_simple.json", "w", encoding="utf-8-sig") as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

# Lưu dữ liệu dạng CSV để mở bằng Excel.
with open("chiaki_simple.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["url", "category", "name", "price", "description", "comments"],
    )
    writer.writeheader()

    for product in products:
        # CSV không lưu list trực tiếp đẹp như JSON,
        # nên chuyển comments từ list thành chuỗi JSON.
        product = product.copy()
        product["comments"] = json.dumps(product["comments"], ensure_ascii=False)
        writer.writerow(product)

print(f"Đã lưu {len(products)} sản phẩm thuốc/thực phẩm chức năng")
