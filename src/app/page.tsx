import Header from "@/components/Header";
import Sidebar from "@/components/Sidebar";
import ProductRanking from "@/components/ProductRanking";

export default function Home() {
  return (
    <div>
      <Header />
      <main className="flex bg-gray-100">
        <Sidebar />
        <ProductRanking />
      </main>
    </div>
  );
}
