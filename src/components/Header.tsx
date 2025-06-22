import { GoLocation } from "react-icons/go";
import { FiSearch, FiShoppingCart } from "react-icons/fi";

const Header = () => {
  return (
    <header>
      {/* Top Header */}
      <div className="bg-[#131921] text-white p-2 flex items-center space-x-4 text-sm">
        {/* Logo */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer">
          <span className="text-2xl font-bold">amazon</span>
          <span className="text-xs">.co.jp</span>
        </div>

        {/* Delivery Address */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer flex items-center">
          <GoLocation className="mt-3" />
          <div className="ml-1">
            <p className="text-xs text-gray-300">お届け先</p>
            <p className="text-sm font-bold">場所を更新する</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-grow flex items-center">
          <select className="bg-gray-200 text-black p-2.5 rounded-l-md text-xs h-10 border-r border-gray-400">
            <option>すべて</option>
          </select>
          <input type="text" className="h-10 p-2 w-full focus:outline-none" />
          <button className="bg-[#F3A847] hover:bg-[#E49B3B] text-black p-2 rounded-r-md h-10">
            <FiSearch size={24} />
          </button>
        </div>
        
        {/* Language */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer flex items-end">
            <p className="text-sm font-bold">JP</p>
        </div>

        {/* Account & Lists */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer">
          <p className="text-xs">こんにちは、ログイン</p>
          <p className="text-sm font-bold">アカウント＆リスト</p>
        </div>

        {/* Returns & Orders */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer">
          <p className="text-xs">返品もこちら</p>
          <p className="text-sm font-bold">注文履歴</p>
        </div>

        {/* Cart */}
        <div className="p-1 border border-transparent hover:border-white cursor-pointer flex items-center">
          <FiShoppingCart size={32} />
          <p className="text-sm font-bold ml-1 mt-3">カート</p>
        </div>
      </div>

      {/* Bottom Header (Navbar) */}
      <div className="bg-[#232F3E] text-white px-4 py-2 flex items-center text-sm space-x-6">
        <p className="font-bold cursor-pointer">すべて</p>
        <p className="cursor-pointer">Amazonポイント: 残高を確認</p>
        <p className="cursor-pointer">ヘルプ</p>
        <p className="cursor-pointer">ネットスーパー</p>
        <p className="cursor-pointer">ランキング</p>
        <p className="cursor-pointer">新着商品</p>
        <p className="cursor-pointer">Amazon Basics</p>
        <p className="cursor-pointer">ミュージック</p>
      </div>
    </header>
  );
};

export default Header; 