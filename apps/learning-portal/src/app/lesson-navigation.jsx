import React from "react";
import { STEP_IDS } from "../routing/portal-router.mjs";

export const STEP_LABELS = Object.freeze({ frame: "Đặt câu hỏi", inspect: "Kiểm tra bằng chứng", run: "Hiểu lượt chạy", fail: "Đọc lỗi có kiểm soát", trace: "Truy vết giới hạn", decide: "Ra quyết định", reset: "Hiểu đặt lại", configure: "Cấu hình giả định", verify: "Hiểu xác minh", reflect: "Phản tư kiến trúc" });

export function LessonNavigation({ current }) {
  return <nav aria-label="Các bước bài học"><h2>Lộ trình tường thuật</h2><ol className="steps">{STEP_IDS.map((id, index) => <li key={id}><a href={`/lesson/promotion-trust/step/${id}`} aria-current={current === id ? "step" : undefined}>{index + 1}. {STEP_LABELS[id]}</a></li>)}</ol></nav>;
}
