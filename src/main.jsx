import React, { useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Battery, BookOpen, ChevronRight, CircleAlert, HeartPulse, Hospital, MapPin, Menu, Navigation, Search, ShieldCheck, SlidersHorizontal, Sparkles, X, Zap } from 'lucide-react'
import './styles.css'

const places = [
  { id: 1, type: 'Тепло', title: 'Пункт незламності «Поруч»', address: 'вул. Велика Васильківська, 72', distance: '0,8 км', hours: 'Відкрито цілодобово', icon: 'heat', accent: 'orange', description: 'Є обігрів, заряджання телефонів, вода та місця для короткого відпочинку.' },
  { id: 2, type: 'Лікарня', title: 'Київська міська лікарня №4', address: 'вул. Солом’янська, 17', distance: '1,4 км', hours: 'Приймальне відділення 24/7', icon: 'hospital', accent: 'red', description: 'Приймальне відділення та пункт першої допомоги. Вхід зі сторони вул. Солом’янської.' },
  { id: 3, type: 'Генератор', title: 'Коворкінг «Світло»', address: 'вул. Антоновича, 44', distance: '1,9 км', hours: 'Сьогодні до 22:00', icon: 'power', accent: 'blue', description: 'Працює генератор, доступні розетки, Wi-Fi не гарантований. Можна зі своїм павербанком.' },
  { id: 4, type: 'Укриття', title: 'Підземний паркінг', address: 'вул. Жилянська, 30', distance: '2,2 км', hours: 'Відкрито під час тривоги', icon: 'shelter', accent: 'green', description: 'Облаштоване укриття на -1 поверсі. Є запас питної води та аптечка.' },
  { id: 5, type: 'Тепло', title: 'Молодіжний центр', address: 'вул. Володимирська, 51', distance: '2,7 км', hours: 'Щодня 08:00–21:00', icon: 'heat', accent: 'orange', description: 'Тепле приміщення, чай, зарядні станції та допомога волонтерів.' },
  { id: 6, type: 'Аптека', title: 'Аптека «Здоров’я»', address: 'вул. Саксаганського, 108', distance: '3,1 км', hours: 'До 20:00', icon: 'pharmacy', accent: 'purple', description: 'Черговий фармацевт та базові засоби першої допомоги.' },
]

const articles = [
  { tag: 'Перша допомога', title: 'Що робити при кровотечі', time: '4 хв читання', text: 'Покроковий алгоритм дій до приїзду медиків: безпека, прямий тиск і контроль стану постраждалого.' },
  { tag: 'Тривожна сумка', title: 'Що покласти в сумку на 24 години', time: '6 хв читання', text: 'Документи, вода, ліки, зарядні пристрої та речі, які справді можуть знадобитися в екстреній ситуації.' },
  { tag: 'Безпека', title: 'Як підготувати телефон до блекауту', time: '3 хв читання', text: 'Налаштування енергоощадження, офлайн-карти та контакти, які варто зберегти заздалегідь.' },
]

const filters = ['Усі', 'Тепло', 'Лікарня', 'Генератор', 'Укриття', 'Аптека']

function PlaceIcon({ type }) {
  const icons = { hospital: Hospital, heat: HeartPulse, power: Zap, shelter: ShieldCheck, pharmacy: CircleAlert }
  const Icon = icons[type] || MapPin
  return <Icon size={19} strokeWidth={2.2} />
}

function App() {
  const [activeFilter, setActiveFilter] = useState('Усі')
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(null)
  const [menuOpen, setMenuOpen] = useState(false)
  const [page, setPage] = useState('map')

  const visiblePlaces = useMemo(() => places.filter((place) => {
    const matchesFilter = activeFilter === 'Усі' || place.type === activeFilter
    const text = `${place.title} ${place.address} ${place.type}`.toLowerCase()
    return matchesFilter && text.includes(query.toLowerCase())
  }), [activeFilter, query])

  const navigate = (nextPage) => { setPage(nextPage); setMenuOpen(false); window.scrollTo({ top: 0, behavior: 'smooth' }) }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand" onClick={() => navigate('map')} role="button" tabIndex="0">
          <div className="brand-mark"><Sparkles size={18} /></div>
          <div><strong>Поруч</strong><span>допомога офлайн</span></div>
        </div>
        <nav className={menuOpen ? 'nav-links open' : 'nav-links'}>
          <button className={page === 'map' ? 'nav-link active' : 'nav-link'} onClick={() => navigate('map')}>Карта допомоги</button>
          <button className={page === 'articles' ? 'nav-link active' : 'nav-link'} onClick={() => navigate('articles')}>Корисне</button>
          <button className="nav-link emergency" onClick={() => setSelected({ title: 'Екстрені номери', address: 'Збережено на пристрої', description: '112 — єдиний номер допомоги, 101 — ДСНС, 102 — поліція, 103 — швидка допомога. У разі небезпеки спочатку подбайте про власну безпеку.' })}>Екстрені номери</button>
        </nav>
        <div className="header-actions"><span className="offline"><span className="status-dot" />Офлайн-режим</span><button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}><Menu size={21} /></button></div>
      </header>

      <main>
        {page === 'map' ? <>
          <section className="hero">
            <div className="hero-copy"><p className="eyebrow">Твоя опора поруч</p><h1>Допомога, коли вона справді потрібна</h1><p className="hero-text">Знайди найближче місце, де можна зігрітися, зарядити телефон, отримати медичну допомогу або перечекати небезпеку. Дані вже збережені на телефоні.</p><div className="hero-stats"><div><strong>42</strong><span>точки поруч</span></div><div><strong>24/7</strong><span>доступ до важливого</span></div><div><strong>0 МБ</strong><span>потрібно для пошуку</span></div></div></div>
            <div className="hero-visual"><div className="map-grid" /><div className="map-label label-a"><span className="pin orange" />Тепло</div><div className="map-label label-b"><span className="pin red" />Лікарня</div><div className="map-label label-c"><span className="pin blue" />Генератор</div><div className="you-marker"><span />Ти тут</div><div className="map-compass"><Navigation size={16} /> N</div></div>
          </section>
          <section className="content-section"><div className="section-heading"><div><p className="eyebrow">Знайти поруч</p><h2>Точки допомоги</h2></div><button className="filter-button"><SlidersHorizontal size={16} /> Фільтри</button></div>
            <div className="search-row"><div className="search-box"><Search size={18} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Пошук за назвою або адресою" /></div><div className="filters">{filters.map((filter) => <button key={filter} className={activeFilter === filter ? 'filter-chip selected' : 'filter-chip'} onClick={() => setActiveFilter(filter)}>{filter}</button>)}</div></div>
            <div className="places-layout"><div className="places-list"><div className="results-count">{visiblePlaces.length} {visiblePlaces.length === 1 ? 'місце' : 'місця'} знайдено <span>· оновлено локально</span></div>{visiblePlaces.map((place) => <article className="place-card" key={place.id} onClick={() => setSelected(place)}><div className={`place-icon ${place.accent}`}><PlaceIcon type={place.icon} /></div><div className="place-info"><div className="place-top"><span className={`type-label ${place.accent}`}>{place.type}</span><span className="distance">{place.distance}</span></div><h3>{place.title}</h3><p><MapPin size={14} />{place.address}</p><small>{place.hours}</small></div><ChevronRight className="card-arrow" size={20} /></article>)}{visiblePlaces.length === 0 && <div className="empty-state">Нічого не знайдено. Спробуй інший запит або категорію.</div>}</div><aside className="mini-map"><div className="mini-map-top"><span>Київ · центр</span><span className="map-legend"><span className="pin orange" /> допомога</span></div><div className="map-road road-1" /><div className="map-road road-2" /><div className="map-road road-3" /><div className="mini-pin p1 orange" /><div className="mini-pin p2 red" /><div className="mini-pin p3 blue" /><div className="mini-pin p4 green" /><div className="mini-you" /><div className="map-scale">500 м</div></aside></div>
          </section>
        </> : <section className="content-section articles-page"><div className="section-heading"><div><p className="eyebrow">Знання без мережі</p><h1>Корисне у складний момент</h1><p className="page-lead">Короткі інструкції, які збережені на пристрої та доступні навіть без інтернету.</p></div></div><div className="article-grid">{articles.map((article) => <article className="article-card" key={article.title}><div className="article-illustration"><BookOpen size={28} /></div><div className="article-content"><span className="article-tag">{article.tag}</span><h3>{article.title}</h3><p>{article.text}</p><div className="article-footer"><span>{article.time}</span><button onClick={() => setSelected({ title: article.title, address: article.time, description: article.text + ' У повній версії тут буде структурований покроковий матеріал із короткими підказками.' })}>Читати <ChevronRight size={15} /></button></div></div></article>)}</div></section>}
      </main>

      <footer><div className="footer-brand"><div className="brand-mark small"><Sparkles size={15} /></div><span>Поруч</span></div><p>Офлайн-застосунок для швидкого доступу до допомоги</p><span className="footer-note">Дані збережені локально на пристрої</span></footer>
      {selected && <div className="modal-backdrop" onClick={() => setSelected(null)}><div className="modal" onClick={(e) => e.stopPropagation()}><button className="modal-close" onClick={() => setSelected(null)}><X size={20} /></button><div className="modal-icon"><PlaceIcon type={selected.icon || 'hospital'} /></div><span className="type-label blue">Інформація поруч</span><h2>{selected.title}</h2><p className="modal-address">{selected.address}</p><p className="modal-description">{selected.description}</p><div className="modal-actions"><button className="primary-btn" onClick={() => setSelected(null)}><MapPin size={17} /> Зрозуміло</button><button className="secondary-btn" onClick={() => setSelected(null)}>Закрити</button></div></div></div>}
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
