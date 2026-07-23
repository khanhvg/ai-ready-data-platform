# Lab junior: metric có trọng số và average-of-averages

## Trạng thái

`candidate-not-runnable`. Đây là candidate Stage A đọc golden rows; không chạy query, không có
runner và không ghi completion.

## Điều kiện tiên quyết

- Dùng đúng source `mart_fulfillment_performance`, grain `(carrier, region_name)`, 25 dòng.
- Fixture read-only có content SHA-256
  `8c0114d1ab48b4fb42009aba3df192988bf917004461d0c0dd0155d0283dce60`.
- `avg_lead_time_days` phải weighting theo `shipment_count - in_transit_count`.
- Giữ nguyên measure cố ý không trọng số `AVG(avg_order_value)` của daily revenue; không sửa mọi
  biểu thức `AVG`.

## Bộ khởi đầu

Tạo bảng riêng với các cột `carrier`, `region_name`, `avg_lead_time_days`, `shipment_count`,
`in_transit_count`, `weight`, `weighted_numerator`. Hai dòng thật đầu tiên để đối chiếu:

| carrier | region_name | avg_lead_time_days | shipment_count | in_transit_count |
|---|---|---:|---:|---:|
| DHL | East Asia | 4.7 | 17 | 0 |
| DHL | Europe | 5.5 | 24 | 3 |

Hoàn thiện đủ 25 dòng từ fixture reader, không copy sang một nguồn truth mới.

## Nhiệm vụ

**Hành động:** tính `weight = shipment_count - in_transit_count`; tính tổng
`avg_lead_time_days * weight`, tổng weight và ratio. Song song tính trung bình đơn giản của 25
group averages để tạo controlled failure.

**Kỳ vọng:** tổng weight là 800; weighted ratio chưa làm tròn là `5.456625`, trong khi invalid
average-of-averages là `5.34`. Hai kết quả phải khác nhau và failure code là
`AVERAGE_OF_AVERAGES_INVALID`.

**Thực tế:** ghi numerator, denominator, correct ratio, invalid result và delta. Không hardcode
failure code thay cho phép tính; verifier tự đọc 25 golden records và tái tính cả hai.

## Lỗi có kiểm soát

Cho mỗi nhóm trọng số bằng 1 và lấy trung bình 25 giá trị. Cách này sai vì số shipment đã giao
trong mỗi nhóm khác nhau. Một lỗi thứ hai là thay luôn `AVG(avg_order_value)` của daily revenue;
verifier phải trả `METRIC_SEMANTIC_DRIFT` vì measure đó được contract giữ cố ý không trọng số.

## Gợi ý 1

In-transit shipment có lead time null nên không thuộc mẫu số. Bắt đầu bằng cột weight, chưa cần
tính ratio.

## Gợi ý 2

Có thể cộng các tử số nhóm nếu cùng định nghĩa: `group_avg * group_weight`. Sau đó chia tổng tử số
cho tổng weight.

## Gợi ý 3

Trọng số xuất phát từ grain và semantics, không từ tên có chữ `avg`. Đọc Rill expression của từng
measure trước khi quyết định.

## Xác minh

Verifier `stage-a.weighted-metrics` đọc source records từ fixture Issue #6, kiểm tra SHA/content,
grain, 25 dòng, weight 800, `5.456625 != 5.34` và bảo vệ hai Rill expressions weighted/unweighted.
Đó là `DL-MET-001` và `DL-MET-002`, không phải runner execution.

## Evidence bất biến

Lưu bảng numerator/denominator và expected/actual tại locator tương đối
`workspace/evidence/weighted-metric-comparison.json`; không lưu raw customer/order rows. Hash cục
bộ phát hiện chỉnh sửa nhưng không chứng minh danh tính publisher. File evidence không tạo
completion.

## Reset

Chỉ xóa bảng công thức trong `workspace/metric-table` thuộc lượt hiện tại, dựng lại starter và giữ
evidence. Không sửa fixture, Rill YAML, dbt SQL hoặc dữ liệu golden.

## Lời giải có khóa

Mở sau ba gợi ý. Công thức đúng là tổng `avg_lead_time_days * (shipment_count -
in_transit_count)` chia tổng `(shipment_count - in_transit_count)`. Với 25 dòng vàng, kết quả là
`5.456625`; trung bình nhóm `5.34` là bằng chứng lỗi.

## Liên kết khắc phục

- `AVERAGE_OF_AVERAGES_INVALID`: dựng lại numerator/denominator ở cùng grain.
- `METRIC_SEMANTIC_DRIFT`: khôi phục source/grain/expression; không áp dụng một quy tắc cho mọi AVG.

## Phản tư đánh đổi

Giữ numerator và denominator làm metric dễ tổng hợp đúng nhưng tăng số measure phải quản trị. Khi
nào một trung bình không trọng số là chủ ý hợp lệ, và contract nào phải nói rõ điều đó?
