# Lab nền tảng: ingest xác định và grain

## Trạng thái

`candidate-not-runnable`. Đây là nội dung Stage A ràng buộc contract để review tĩnh. Nó không có
runner, không ghi progress và không chứng minh một trải nghiệm học tập đã hoàn thành.

## Điều kiện tiên quyết

- Chỉ đọc `contracts/data/retail-golden-v1.json` và reader Issue #6.
- Profile phải là `small`, seed phải là `42`.
- Golden hiện có 18 CSV, tổng 6.812 dòng. Grain landing là một dòng CSV trong đúng raw table.
- Mọi lỗi được tạo trong `workspace/input-copy`; không sửa `data-generator`, contract hoặc fixture.

## Bộ khởi đầu

Tạo bảng làm việc riêng gồm các cột `file`, `row_count`, `csv_sha256`. Điền trước hai dòng từ
projection reader, để trống 16 dòng còn lại. Ghi thêm `ordered_summary_sha256` và
`manifest_projection_sha256` ở cuối bảng. Đây là artifact người học phải thay đổi, không phải bài
đọc cuộn trang.

## Nhiệm vụ

**Hành động:** hoàn thiện bảng 18 tệp từ projection `small`/42, cộng `row_count`, rồi mô tả grain
của `orders.csv` và `order_items.csv` bằng hai câu riêng. Tạo một bản sao riêng của một dòng bảng,
đổi checksum nhưng giữ nguyên tổng dòng để kích hoạt lỗi.

**Kỳ vọng:** tổng là 6.812; `file_count` là 18; projection theo thứ tự có SHA-256
`60ce82ce297acec1e3c047466f4b068baed5dc1875964832cb6cda3d4f91e9d6`; lỗi riêng trả
`GOLDEN_INPUT_MISMATCH`.

**Thực tế:** ghi số đếm, SHA-256 quan sát được và failure code vào bảng evidence. Nếu khác kỳ
vọng, giữ cả hai giá trị; không sửa golden để làm cho chúng bằng nhau.

## Lỗi có kiểm soát

Chỉ đổi checksum trong bản sao `workspace/input-copy`. Việc giữ đúng tổng 6.812 nhưng sai một
checksum chứng minh row count không đủ để nhận diện input. Boundary là workspace-only; một thay
đổi ở tệp vàng phải trả `PROTECTED_GOLDEN_DRIFT` và dừng.

## Gợi ý 1

Bắt đầu từ `generator.fileCount`, `generator.totalRows` và hai projection hash trong retail golden
contract; chưa cần nhìn model.

## Gợi ý 2

Đối chiếu theo cặp `(file, row_count, csv_sha256)`. Sắp xếp khác thứ tự cũng làm projection tổng
khác dù từng checksum riêng đúng.

## Gợi ý 3

`orders.csv` có grain order, còn `order_items.csv` có grain order line. Một order có thể có nhiều
order item, vì vậy không được so row count của hai bảng như cùng grain.

## Xác minh

Verifier `stage-a.deterministic-ingest` kiểm tra `DL-ING-001` và `DL-PROT-001`: profile/seed,
18/6.812, projection hashes, descriptor `lab-v1`, cặp content và toàn bộ protected hashes. Static
pass chỉ xác nhận candidate nhất quán; không chạy ingest.

## Evidence bất biến

Artifact chỉ gồm stable ID, expected/actual, SHA-256 và locator tương đối
`workspace/evidence/ingest-comparison.json`. Không lưu raw row, full environment, thông tin nhận
dạng hay locator máy cá nhân. Sự hiện diện của file evidence không tạo completion.

## Reset

Xóa đúng workspace có owner marker của lượt hiện tại rồi tạo lại bảng starter. Không clean repo,
không theo glob rộng, không xóa state không thuộc lượt. Evidence review-bundle được giữ; progress
không đổi.

## Lời giải có khóa

Chỉ mở sau ba gợi ý. Bảng đúng có 18 dòng, tổng 6.812 và hai projection hash nêu trên; checksum bị
đổi phải thất bại dù tổng dòng không đổi. Lời giải tách khỏi starter và không tự xác minh.

## Liên kết khắc phục

- `GOLDEN_INPUT_MISMATCH`: tạo lại bản sao riêng và so từng tuple file/count/hash.
- `PROTECTED_GOLDEN_DRIFT`: dừng, giữ evidence và phục hồi đúng Git object phát hành.

## Phản tư đánh đổi

Checksum giúp tái lập và phát hiện drift, nhưng chỉ chứng minh toàn vẹn cục bộ, không chứng minh
ai đã phát hành dữ liệu. Khi nào row count đủ cho health check, và khi nào cần content hash?
