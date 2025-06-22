import ProductCard from "./ProductCard";

const dummyProducts = [
  {
    rank: 1,
    imageUrl: "https://via.placeholder.com/200",
    title: "Nintendo Switch 2(日本語・国…",
    rating: 4.5,
    reviewCount: 660,
  },
  {
    rank: 2,
    imageUrl: "https://via.placeholder.com/200",
    title: "たまごっちのプッチプチおみせっち～にんきのおみせあつめちゃいました～ -Switch",
    rating: 4.0,
    reviewCount: 120,
  },
  {
    rank: 3,
    imageUrl: "https://via.placeholder.com/200",
    title: "対応 Switch2 ガラスフィルム ガイド枠付き 【Seninhi 】【2枚セット 日本旭硝子製 高 品質 】対応…",
    rating: 4.5,
    reviewCount: 2500,
  },
  {
    rank: 4,
    imageUrl: "https://via.placeholder.com/200",
    title: "Switch 2 ガラスフィルム 2025 ohyes Switch 2 フィルム 強化ガラス Switch 2 保護フィルム スイ…",
    rating: 4.0,
    reviewCount: 890,
  },
];

const ProductRanking = () => {
  return (
    <div className="p-4 flex-grow">
        <div className="flex justify-between items-baseline mb-2">
            <h1 className="text-2xl font-bold">ゲームの売れ筋ランキング</h1>
            <a href="#" className="text-sm text-blue-600 hover:text-orange-500 hover:underline">もっと見る</a>
        </div>
      <div className="flex items-start">
        {dummyProducts.map((product) => (
          <ProductCard
            key={product.rank}
            rank={product.rank}
            imageUrl={product.imageUrl}
            title={product.title}
            rating={product.rating}
            reviewCount={product.reviewCount}
          />
        ))}
      </div>
      <div className="text-right mt-2">
        <span className="text-sm">ページ: 1 / 5</span>
      </div>
    </div>
  );
};

export default ProductRanking; 