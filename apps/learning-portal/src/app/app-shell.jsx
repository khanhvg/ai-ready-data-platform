import React from 'react';

const A = ({ href, onNavigate, children, className }) => <a href={href} onClick={onNavigate} className={className}>{children}</a>;
const List = ({ items }) => <ul>{items.map((item) => <li key={typeof item === 'string' ? item : JSON.stringify(item)}>{typeof item === 'string' ? item : JSON.stringify(item)}</li>)}</ul>;
const Text = ({ children }) => <p className="source-text">{children}</p>;

function Breadcrumbs({ route, onNavigate }) {
  const parent = route.kind === 'module' ? ['/curriculum', 'Lộ trình học'] : route.kind === 'lab' ? ['/labs', 'Lab thủ công'] : route.kind.startsWith('promotion') ? ['/curriculum', 'Lộ trình học'] : ['/', 'Trang chủ'];
  return <nav aria-label="Đường dẫn"><ol className="breadcrumbs"><li><A href="/" onNavigate={onNavigate}>Trang chủ</A></li>{route.path !== '/' && parent[0] !== '/' && <li><A href={parent[0]} onNavigate={onNavigate}>{parent[1]}</A></li>}{route.path !== '/' && <li aria-current="page">{route.label}</li>}</ol></nav>;
}

function Home({ catalog, onNavigate }) {
  return <>
    <p className="kicker">Đọc · hiểu · tự thực hành tại local</p>
    <h1>Nền tảng dữ liệu sẵn sàng cho AI</h1>
    <p className="lede">Một sản phẩm học tập chỉ đọc bằng tiếng Việt: 20 mô-đun kiến trúc, 5 góc nhìn nguồn, và 3 lab hướng dẫn thủ công. Website không chạy lệnh và không ghi nhận hoàn thành.</p>
    <div className="stats" aria-label="Phạm vi phát hành"><span><strong>{catalog.counts.modules}</strong> mô-đun</span><span><strong>{catalog.counts.views}</strong> sơ đồ</span><span><strong>{catalog.counts.labs}</strong> lab thủ công</span></div>
    <div className="card-grid">
      <article><p className="tag">01 · Học theo cấp độ</p><h2>Lộ trình kiến trúc</h2><p>Từ nền tảng tới mid-level, đi qua concern, FR/NFR, trade-off và vận hành.</p><A href="/curriculum" onNavigate={onNavigate} className="text-link">Mở lộ trình →</A></article>
      <article><p className="tag">02 · Đọc hệ thống</p><h2>Năm góc nhìn</h2><p>Container, deployment và ba luồng động có text alternative đầy đủ.</p><A href="/architecture" onNavigate={onNavigate} className="text-link">Xem kiến trúc →</A></article>
      <article><p className="tag">03 · Tự làm</p><h2>Lab tại local</h2><p>Lệnh có thể sao chép dưới dạng văn bản; chính bạn chạy trong terminal riêng.</p><A href="/labs" onNavigate={onNavigate} className="text-link">Đọc hướng dẫn →</A></article>
    </div>
    <aside className="notice"><strong>Phạm vi an toàn:</strong> không runner, không Docker, không cloud, không progress, không thao tác ghi.</aside>
  </>;
}

function Curriculum({ catalog, onNavigate }) {
  return <><p className="kicker">Lộ trình phát hành</p><h1>20 mô-đun, bốn cấp độ</h1><p className="lede">Học theo thứ tự foundation → junior → data → mid. Mỗi mô-đun là một bài đọc độc lập và một thought exercise có kiểm soát.</p><nav className="toc" aria-label="Mục lục lộ trình">{catalog.curriculum.collections.map((collection) => <a key={collection.id} href={`#${collection.id}`}>{collection.label}</a>)}</nav>
    {catalog.curriculum.collections.map((collection) => <section key={collection.id} id={collection.id}><div className="section-heading"><p className="tag">{collection.modules.length} mô-đun</p><h2>{collection.label}</h2></div><div className="module-list">{collection.modules.map((module) => <A key={module.id} href={`/curriculum/${module.id.toLowerCase()}`} onNavigate={onNavigate} className="module-row"><span className="module-id">{module.id}</span><span><strong>{module.outcome}</strong><small>{module.capability}</small></span><span aria-hidden="true">→</span></A>)}</div></section>)}
    <aside className="notice">Bài đọc mẫu: <A href="/lessons/promotion-trust" onNavigate={onNavigate}>Độ tin cậy của quyết định khuyến mãi</A>.</aside>
  </>;
}

function ModulePage({ module }) {
  const consequences = module.operationsConsequence;
  const checklist = [module.verify.verifier, module.evidence.required, ...module.requiredViews.map((id) => `Đối chiếu góc nhìn ${id}`)];
  return <><p className="kicker">{module.collectionLabel} · Mô-đun {module.id}</p><h1>{module.outcome}</h1><p className="lede">{module.capability}</p>
    <nav className="toc" aria-label="Mục lục bài học"><strong>Trong bài này</strong><a href="#context">Bối cảnh</a><a href="#decision">Quyết định</a><a href="#exercise">Bài tập tư duy</a><a href="#verify">Xác minh</a><a href="#reflect">Phản tư</a></nav>
    <section id="context"><h2>Bối cảnh và yêu cầu</h2><dl className="facts"><div><dt>Concern của stakeholder</dt><dd>{module.concern}</dd></div><div><dt>Functional requirement</dt><dd>{module.requirements.functional}</dd></div><div><dt>Non-functional requirement</dt><dd>{module.requirements.nonFunctional}</dd></div><div><dt>Artifact</dt><dd><code>{module.artifact}</code></dd></div></dl></section>
    <section id="decision"><h2>Quyết định và hệ quả</h2><h3>Phương án / trade-off</h3><List items={module.options}/><p><strong>ADR / pattern:</strong> <code>{module.adrOrPattern}</code></p><p><strong>Implementation intent:</strong> {module.implementationIntent}</p><p><strong>Góc nhìn bắt buộc:</strong> {module.requiredViews.join(', ')}</p><div className="consequence-grid">{['operations','security','resilience','cost','governance'].map((key) => <div key={key}><strong>{key}</strong><span>{consequences[key]}</span></div>)}</div></section>
    <section id="exercise"><h2>Thought exercise có kiểm soát</h2><h3>Starter</h3><Text>{module.starter.prompt}</Text><h3>Nhiệm vụ</h3><Text>{module.task.instruction}</Text><h3>Controlled failure</h3><Text>{module.controlledFailure.scenario}</Text><p className="manual-label">Chỉ suy luận trên giấy / workspace riêng · website không thực thi</p><h3>Gợi ý</h3><ol>{module.hints.map(({ order, text }) => <li key={order}>{text}</li>)}</ol><details><summary>Lời giải tham chiếu — mở sau khi đã dùng gợi ý</summary><p>{module.solution.intent}</p><p>Gate: <code>{module.solution.revealGate}</code></p></details></section>
    <section id="verify"><h2>Checklist xác minh</h2><List items={checklist}/><h3>Reset an toàn</h3><Text>{module.reset.procedure}</Text><p>Chỉ khôi phục bản nháp của bài tập; không clean repo hoặc xóa state ngoài phạm vi.</p></section>
    <section id="reflect"><h2>Phản tư đánh đổi</h2><Text>{module.tradeOffReflection.reflection}</Text><p><strong>Forces:</strong> {module.tradeOffReflection.forces.join(' · ')}</p></section>
  </>;
}

function Architecture({ catalog }) {
  const { trace, templates, patterns, views } = catalog.architecture;
  return <><p className="kicker">Architecture trace</p><h1>Năm góc nhìn từ source</h1><p className="lede">Mỗi SVG được xác minh hash từ authority phát hành, co giãn theo màn hình và đi kèm mô tả văn bản.</p>
    <nav className="toc" aria-label="Mục lục kiến trúc"><a href="#views">Góc nhìn</a><a href="#flows">11 critical flow</a><a href="#bridges">8 bridge</a><a href="#templates">Template và pattern</a></nav>
    <section id="views">{views.map((view) => <figure className="architecture-view" key={view.id}><div className="figure-title"><span className="module-id">{view.id}</span><div><h2>{view.concern}</h2><p>{view.abstraction} · {view.purpose}</p></div></div><img src={view.assetPath} alt={`Sơ đồ ${view.id}: ${view.concern}`} width="1200" height="800" loading="lazy" /><figcaption>{view.concern}. <a href={`${view.assetPath.replace('.svg', '.txt')}`}>Mở text alternative</a>.</figcaption><details><summary>Nội dung thay thế dạng văn bản</summary><pre><code>{view.text}</code></pre></details></figure>)}</section>
    <section id="flows"><h2>11 critical flow</h2><div className="card-grid compact">{catalog.curriculum.criticalFlows.map((flow) => <article key={flow.id}><p className="tag">{flow.viewId}</p><h3>{flow.id}</h3><ol>{flow.steps.map((step) => <li key={step}>{step}</li>)}</ol></article>)}</div></section>
    <section id="bridges"><h2>8 bridge local ↔ AWS</h2><div className="module-list">{trace.bridges.map((bridge) => <div className="module-row static" key={bridge.id}><span className="module-id">{bridge.id.replace('BR-','')}</span><span><strong>{bridge.claimClass}</strong><small>{bridge.divergence}</small></span></div>)}</div></section>
    <section id="templates"><h2>Template và pattern</h2><p>{templates.templates.length} template có version và content hash; {patterns.patterns.length} pattern được admission.</p><div className="card-grid compact">{templates.templates.map((template) => <article key={template.id}><p className="tag">v{template.version}</p><h3>{template.id}</h3><p>{template.purpose}</p></article>)}</div><h3>{patterns.adr.id}</h3><p>{patterns.adr.status}: {patterns.adr.consequences.join(' · ')}</p><List items={patterns.patterns.map((pattern) => `${pattern.id}: ${pattern.force} → ${pattern.failure}`)}/></section>
  </>;
}

function Labs({ catalog, onNavigate }) {
  return <><p className="kicker">Manual labs</p><h1>Ba lab tự thực hành tại local</h1><p className="lede">Đọc hướng dẫn, sao chép lệnh và tự chạy trong terminal của bạn. Website không kết nối terminal, không chạy lệnh và không tuyên bố hoàn thành.</p><div className="card-grid">{catalog.labs.map((lab, index) => <article key={lab.slug}><p className="tag">Lab {String(index + 1).padStart(2,'0')}</p><h2>{lab.title}</h2><p><code>{lab.descriptor.id}</code> · profile {lab.descriptor.profile.id}/{lab.descriptor.profile.seed}</p><A href={`/labs/${lab.slug}`} onNavigate={onNavigate} className="text-link">Mở hướng dẫn →</A></article>)}</div></>;
}

function LabPage({ lab }) {
  const get = (name) => lab.sections[name] ?? '';
  return <><p className="manual-label">Thực hành thủ công tại local</p><h1>{lab.title}</h1><p className="lede">Website chỉ trình bày hướng dẫn. Bạn quyết định khi nào chạy từng lệnh trong terminal local; không có completion state.</p>
    <nav className="toc" aria-label="Mục lục lab"><a href="#prerequisites">Điều kiện</a><a href="#starter">Starter</a><a href="#task">Nhiệm vụ</a><a href="#commands">Lệnh</a><a href="#failure">Lỗi có kiểm soát</a><a href="#verify">Xác minh</a><a href="#reset">Reset</a></nav>
    <section id="prerequisites"><h2>Điều kiện tiên quyết</h2><Text>{get('Điều kiện tiên quyết')}</Text></section>
    <section id="starter"><h2>Bộ khởi đầu</h2><Text>{get('Bộ khởi đầu')}</Text></section>
    <section id="task"><h2>Nhiệm vụ</h2><Text>{get('Nhiệm vụ')}</Text></section>
    <section id="commands"><h2>Lệnh terminal hiện có trong repo</h2><p>Chạy thủ công từ repository root, từng lệnh một. Các khối dưới đây là văn bản, không phải nút thực thi.</p>{lab.commands.map((command) => <pre className="command" key={command}><code>{command}</code></pre>)}</section>
    <section id="failure"><h2>Lỗi có kiểm soát</h2><Text>{get('Lỗi có kiểm soát')}</Text></section>
    <section><h2>Gợi ý</h2>{['Gợi ý 1','Gợi ý 2','Gợi ý 3'].map((name) => <details key={name}><summary>{name}</summary><Text>{get(name)}</Text></details>)}</section>
    <section id="verify"><h2>Expected checks và evidence</h2><Text>{get('Xác minh')}</Text><Text>{get('Evidence bất biến')}</Text><p>Giữ expected và actual tách biệt; website không đọc evidence và không đánh dấu pass.</p></section>
    <section id="reset"><h2>Reset an toàn, đúng phạm vi</h2><Text>{get('Reset')}</Text><p>Không dùng broad cleanup. Nếu repo không cung cấp target reset đúng workspace, thực hiện đúng mô tả owner-marker thay vì tự bịa lệnh.</p></section>
    <section><h2>Solution gate</h2><p>Chỉ mở sau khi đã đọc và thử cả ba gợi ý.</p><details><summary>Mở lời giải có khóa</summary><Text>{get('Lời giải có khóa')}</Text></details><h2>Phản tư trade-off</h2><Text>{get('Phản tư đánh đổi')}</Text></section>
  </>;
}

function Promotion({ catalog, route, onNavigate }) {
  const lesson = catalog.promotionTrust.lesson;
  const step = lesson.narrativeSteps.find(({ id }) => id === route.stepId);
  return <><p className="kicker">Bài đọc mẫu phát hành</p><h1>{catalog.promotionTrust.title}</h1><p className="lede">{lesson.summary}</p><aside className="notice">Kết luận nguồn: <strong>{lesson.decision.status}</strong>. Bốn grain độc lập không đủ chứng minh quan hệ nhân quả chiến dịch.</aside>{step ? <section><h2>Bước {step.order}: {step.id}</h2><p>Static equivalent: {String(step.staticEquivalent)} · reversible: {String(step.reversible)}.</p></section> : <><section><h2>Câu hỏi quyết định</h2><p>{lesson.decision.question}</p><p>Chọn: <code>{lesson.decision.selected}</code></p></section><section><h2>10 bước đọc</h2><div className="module-list">{lesson.narrativeSteps.map((item) => <A key={item.id} href={`/lessons/promotion-trust/steps/${item.id}`} onNavigate={onNavigate} className="module-row"><span className="module-id">{item.order}</span><strong>{item.id}</strong><span>→</span></A>)}</div></section></>}</>;
}

export function AppShell({ catalog, route, onNavigate }) {
  const module = route.moduleId && catalog.curriculum.modules.find(({ id }) => id === route.moduleId);
  const lab = route.labSlug && catalog.labs.find(({ slug }) => slug === route.labSlug);
  return <div className="portal-shell" data-read-only="true" data-manual-only="true" data-semantic-ready="true">
    <a className="skip-link" href="#main-content">Bỏ qua điều hướng</a>
    <header className="masthead"><A href="/" onNavigate={onNavigate} className="brand"><span className="brand-mark">AI</span><span>Data Learning<br/><small>Read-only portal</small></span></A><nav aria-label="Điều hướng chính"><A href="/curriculum" onNavigate={onNavigate}>Lộ trình</A><A href="/architecture" onNavigate={onNavigate}>Kiến trúc</A><A href="/labs" onNavigate={onNavigate}>Lab thủ công</A></nav></header>
    <div className="page"><Breadcrumbs route={route} onNavigate={onNavigate}/><main id="main-content" tabIndex="-1">
      {route.kind === 'home' && <Home catalog={catalog} onNavigate={onNavigate}/>}
      {route.kind === 'curriculum' && <Curriculum catalog={catalog} onNavigate={onNavigate}/>}
      {route.kind === 'module' && <ModulePage module={module}/>}
      {route.kind === 'architecture' && <Architecture catalog={catalog}/>}
      {route.kind === 'labs' && <Labs catalog={catalog} onNavigate={onNavigate}/>}
      {route.kind === 'lab' && <LabPage lab={lab}/>}
      {route.kind.startsWith('promotion') && <Promotion catalog={catalog} route={route} onNavigate={onNavigate}/>}
    </main><nav className="pager" aria-label="Bài trước và bài sau">{route.previous && <A href={route.previous.path} onNavigate={onNavigate}>← {route.previous.label}</A>}{route.next && <A href={route.next.path} onNavigate={onNavigate}>{route.next.label} →</A>}</nav></div>
    <footer><p>Stage A · đọc và học · manual-only</p><p>Không runner · không storage · không cloud</p></footer>
  </div>;
}
