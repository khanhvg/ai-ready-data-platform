export function PromotionTrustLesson({ viewModel }) {
  const { lesson, sourceGrains, step } = viewModel;
  if (!lesson) return null;
  return (
    <article className="lesson-card" aria-labelledby="lesson-title">
      <header><p className="section-label">Bài học đại diện</p><h2 id="lesson-title">{lesson.titleVi ?? lesson.title}</h2><p className="lede">{lesson.summaryVi ?? lesson.summary}</p></header>
      {step ? <section className="selected-step" aria-labelledby="selected-step-title"><p className="section-label">Đang xem</p><h3 id="selected-step-title">Bước {step.order}: {step.id}</h3><p>Bước tường thuật này có bản tương đương tĩnh. Không có lệnh chạy, đặt lại, xác minh hay ghi nhận tiến độ trong Stage A.</p></section> : null}
      <section aria-labelledby="decision-title"><p className="section-label">Kết luận được phát hành</p><h3 id="decision-title">{lesson.decision.question}</h3><p className="decision" data-fact-id={`decision-${lesson.decision.status}`}>{lesson.decision.status}</p><p>Giữ bốn grain độc lập là lựa chọn đúng. Không có grain chung để quy kết quan hệ nhân quả giữa chiến dịch và kết quả vận hành.</p></section>
      <section aria-labelledby="grains-title"><p className="section-label">Bốn grain độc lập</p><h3 id="grains-title">Phạm vi bằng chứng</h3><div className="grain-grid">{sourceGrains.map((grain) => <article className="grain-card" data-fact-id={`grain-${grain.id}`} key={grain.id}><h4>{grain.displayId}</h4><p>Khóa: {grain.keys.join(' · ')}</p><p>Không được nối suy diễn với ba grain còn lại.</p></article>)}</div></section>
      <section aria-labelledby="limits-title"><p className="section-label">Giới hạn</p><h3 id="limits-title">Điều bằng chứng không chứng minh</h3><ul>{lesson.limitations.map((limitation) => <li data-fact-id={`limitation-${limitation.id}`} key={limitation.id}><strong>{limitation.id}</strong>: {limitation.statement}</li>)}</ul></section>
      <section aria-labelledby="hints-title"><p className="section-label">Gợi ý theo thứ tự</p><h3 id="hints-title">Quan sát trước khi kết luận</h3><ol>{lesson.hints.map((hint) => <li key={hint.id}>{hint.order}. {hint.id} — chỉ hướng dẫn, không hoàn thành bài.</li>)}</ol></section>
      <section className="reflection" aria-labelledby="reflection-title"><p className="section-label">Phản tư về đánh đổi</p><h3 id="reflection-title">{lesson.reflection.prompt}</h3><p>Thêm một grain có thể hỗ trợ quy kết, nhưng chỉ khi được phát hành qua hợp đồng đã duyệt. Stage A không tự tạo khóa chiến dịch, đơn hàng hay thời gian.</p></section>
    </article>
  );
}
