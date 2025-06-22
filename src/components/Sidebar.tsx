const Sidebar = () => {
  const categories = [
    "Amazonデバイス・アクセサリ",
    "Amazon整備済み品",
    "DIY・工具・ガーデン",
    "DVD",
    "Kindleストア",
    "PCソフト",
    "Prime Video",
    "アプリ＆ゲーム",
    "おもちゃ",
    "ギフトカード",
    "ゲーム",
    "スポーツ＆アウトドア",
    "デジタルミュージック",
    "ドラッグストア",
  ];

  return (
    <aside className="w-64 p-4">
      <h2 className="font-bold text-base mb-2">すべてのカテゴリー</h2>
      <ul>
        {categories.map((category) => (
          <li key={category} className="mb-1">
            <a href="#" className="text-sm hover:text-orange-500 hover:underline">
              {category}
            </a>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar; 