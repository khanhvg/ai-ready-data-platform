# Lab junior: lớp mô hình và chất lượng có chủ đích

## Trạng thái

`candidate-not-runnable`. Stage A chỉ kiểm tra contract và nội dung; không gọi dbt, không có
runner, không ghi progress và không tuyên bố learner journey đã hoàn thành.

## Điều kiện tiên quyết

- Chỉ đọc model, test và reader Issue #6 ở profile `small`, seed `42`.
- Golden graph có 18 source, 18 staging, 6 intermediate, 16 core, 11 mart và tổng 51 model.
- Golden build có 141 generic test; kết quả 179 pass, 7 warn, 0 fail, tổng 186.
- Chín test được cấu hình warn; quan sát thực tế là bảy warn và hai pass. Không đổi severity.

## Bộ khởi đầu

Tạo artifact `model-map` riêng gồm năm cột: `source`, `staging`, `intermediate`, `core`, `mart`;
thêm `grain`, `quality_identity`, `configured_severity`, `observed_status`. Starter cố ý để trống
intermediate/core và gắn một warning vào cột error để người học sửa bằng evidence.

## Nhiệm vụ

**Hành động:** hoàn thiện một đường
`source -> staging -> intermediate -> core -> mart` cho fulfillment, ghi grain tại mỗi lớp; sau
đó phân loại một controlled invalid status, một dangling product relationship và một test warning
được cấu hình nhưng pass trên input này.

**Kỳ vọng:** graph projection SHA-256 là
`9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df`; build là
179 pass / 7 warn / 0 fail / 186 total; warning có kiểm soát không bị nâng thành error và cũng
không bị bỏ qua.

**Thực tế:** lưu path, grain, configured severity và observed status riêng biệt. Nếu actual khác,
ghi `MODEL_GRAIN_MISMATCH`, `QUALITY_WARNING_MISMATCH` hoặc `QUALITY_SEVERITY_DRIFT`; không sửa
YAML/SQL vàng.

## Lỗi có kiểm soát

Trong bản đồ riêng, đổi một warning thành error hoặc gắn `mart_fulfillment_performance` vào grain
order line. Verifier phải bắt lỗi mapping, trong khi protected `transform/dbt` giữ nguyên. Mất
tool/runtime là lỗi môi trường, không phải controlled warning.

## Gợi ý 1

Source và staging thường cùng business entity nhưng staging làm sạch/dedupe. Hãy ghi grain trước
khi nối các hộp.

## Gợi ý 2

Intermediate giữ logic tái sử dụng; core là interface dimensional/fact ổn định; mart mới là grain
phục vụ business. Với fulfillment, bắt đầu từ shipment rồi tìm store region.

## Gợi ý 3

`configured severity = warn` và `observed status = pass` không mâu thuẫn. Chín cấu hình warning
không có nghĩa mọi input phải tạo chín warning.

## Xác minh

Verifier `stage-a.model-quality` kiểm tra `DL-MOD-001`, `DL-DQ-001`, `DL-DQ-002`, các count/hash
golden, descriptor `lab-v1`, lifecycle và remediation mapping. Static pass không thay thế một lần
dbt build có runner.

## Evidence bất biến

Ghi stable assertion ID, expected/actual count, graph hash và locator tương đối
`workspace/evidence/model-quality-comparison.json`. Không chép raw row, log đầy đủ hay cấu hình
riêng của máy. File evidence, hint hoặc lời giải không có quyền set completion.

## Reset

Xóa đúng `workspace/model-map` có owner marker của lượt hiện tại, dựng lại starter và giữ evidence.
Không sửa model/test, không xóa target ngoài workspace, không dùng broad repository cleanup.

## Lời giải có khóa

Mở sau ba gợi ý. Một path hợp lệ là raw shipments → staging shipment → intermediate fulfillment
→ core shipment fact kết hợp order/store dimension → fulfillment mart, với grain cuối
`carrier, region_name`. Phân loại đúng giữ configured/observed tách biệt.

## Liên kết khắc phục

- `MODEL_GRAIN_MISMATCH`: đối chiếu lại từng layer và grain trước khi nối.
- `QUALITY_WARNING_MISMATCH`: tách controlled warning khỏi lỗi môi trường và unexpected error.
- `QUALITY_SEVERITY_DRIFT`: dừng nếu YAML/SQL vàng thay đổi; chỉ sửa artifact riêng.

## Phản tư đánh đổi

Warning giữ demo có dữ liệu xấu quan sát được, nhưng quá nhiều warning dễ che lỗi thật. Khi nào
nên nâng một test thành error, và evidence nào cần có trước quyết định đó?
