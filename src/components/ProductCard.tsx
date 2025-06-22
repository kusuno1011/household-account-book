import Image from "next/image";
import { FaStar, FaStarHalfAlt } from "react-icons/fa";

type ProductCardProps = {
  rank: number;
  imageUrl: string;
  title: string;
  rating: number;
  reviewCount: number;
};

const ProductCard = ({
  rank,
  imageUrl,
  title,
  rating,
  reviewCount,
}: ProductCardProps) => {
  const renderStars = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= rating) {
        stars.push(<FaStar key={i} className="text-yellow-500" />);
      } else if (i - 0.5 <= rating) {
        stars.push(<FaStarHalfAlt key={i} className="text-yellow-500" />);
      } else {
        stars.push(<FaStar key={i} className="text-gray-300" />);
      }
    }
    return stars;
  };

  return (
    <div className="flex flex-col items-center text-center p-4">
      <span className="text-3xl font-bold text-orange-700 self-start">#{rank}</span>
      <Image src={imageUrl} alt={title} width={200} height={200} className="my-2" />
      <h3 className="text-blue-600 hover:text-orange-500 hover:underline cursor-pointer text-sm">
        {title}
      </h3>
      <div className="flex items-center mt-1">
        {renderStars()}
        <span className="ml-2 text-blue-600 hover:text-orange-500 cursor-pointer text-sm">{reviewCount}</span>
      </div>
    </div>
  );
};

export default ProductCard; 