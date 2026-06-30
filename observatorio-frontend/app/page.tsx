"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [resultados, setResultados] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [buscou, setBuscou] = useState(false);

  const executarBusca = async () => {
    if (!query) return;
    setLoading(true);
    setBuscou(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/buscar-pesquisadores", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
      });
      const data = await response.json();
      setResultados(data.resultados || []);
    } catch (error) {
      console.error("Erro na busca:", error);
      setResultados([]);
    }
    setLoading(false);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-start bg-zinc-950 text-zinc-100 p-8 md:p-12 font-sans">
      
      {/* Cabeçalho */}
      <div className="mt-4 text-center">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-cyan-300 pb-2 drop-shadow-sm">
          Observatório CTI
        </h1>
        <p className="mt-2 text-base text-zinc-400 max-w-2xl mx-auto">
          O grimório definitivo das produções científicas e dados vetoriais.
        </p>
      </div>

      {/* Barra de Busca */}
      <div className="mt-8 w-full max-w-3xl">
        <div className="relative flex items-center w-full h-14 rounded-md focus-within:ring-2 focus-within:ring-cyan-500 bg-zinc-900/80 border border-zinc-700 shadow-[0_0_15px_rgba(6,182,212,0.15)]">
          <input
            className="h-full w-full outline-none text-base text-zinc-100 bg-transparent px-6 placeholder-zinc-600 font-medium"
            placeholder="Digite nome (ex: Eduardo) ou tema..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && executarBusca()}
          />
          <button 
            onClick={executarBusca}
            className="h-full px-6 md:px-8 bg-cyan-700 hover:bg-cyan-600 transition-colors text-white font-bold text-sm uppercase tracking-widest rounded-r-md border-l border-cyan-500"
          >
            {loading ? "LENDO..." : "BUSCAR"}
          </button>
        </div>
      </div>

      {/* Mensagem de Vazio */}
      {buscou && !loading && resultados.length === 0 && (
        <p className="mt-12 text-zinc-500 italic text-lg animate-pulse">
          O grimório silencia. Nenhuma alma acadêmica encontrada para esta busca.
        </p>
      )}

      {/* Grid de Resultados */}
      {resultados.length > 0 && (
        <div className="mt-12 w-full max-w-7xl grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {resultados.map((pesquisador, index) => (
            <div 
              key={index}
              className={`relative flex flex-col bg-zinc-900 border-2 rounded-sm p-1 transition-all duration-300 shadow-xl group
                ${index === 0 ? "border-cyan-600 shadow-[0_0_20px_rgba(6,182,212,0.2)]" : "border-zinc-800 hover:border-cyan-800"}`}
            >
              <div className="border border-zinc-700/50 p-5 h-full flex flex-col bg-gradient-to-b from-zinc-800/50 to-zinc-900/50">
                
                {/* Header: Avatar + Info */}
                <div className="flex gap-4 mb-4 items-start">
                  <div className={`w-16 h-16 shrink-0 rounded-md border-2 bg-zinc-800 overflow-hidden shadow-inner transition-colors
                    ${index === 0 ? "border-cyan-500" : "border-zinc-600 group-hover:border-cyan-700"}`}>
                    <img 
                      src={`https://api.dicebear.com/8.x/bottts/svg?seed=${pesquisador.nome}&backgroundColor=27272a`} 
                      alt="Avatar"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h2 className="text-lg font-bold text-zinc-100 leading-tight truncate" title={pesquisador.nome}>
                      {pesquisador.nome}
                    </h2>
                    <p className={`text-[11px] font-semibold uppercase tracking-wider mt-1
                      ${index === 0 ? "text-cyan-400" : "text-cyan-600"}`}>
                      Classe: {pesquisador.classe_criativa}
                    </p>
                  </div>
                </div>

                {/* Tags de Temas */}
                <div className="mb-4 flex flex-wrap gap-2">
                  {pesquisador.temas.map((tema: string, tIndex: number) => (
                    <span key={tIndex} className="bg-zinc-950 border border-zinc-800 text-zinc-300 px-2 py-1 text-[10px] uppercase tracking-wide rounded-full font-medium">
                      {tema}
                    </span>
                  ))}
                </div>

                {/* Atributos Básicos */}
                <div className="grid grid-cols-2 gap-3 pb-4 border-b border-zinc-700/50 mb-4">
                  <div className="flex flex-col items-center bg-zinc-950 border border-zinc-800 rounded p-2">
                    <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-1">Índice H</span>
                    <span className="text-xl font-black text-white">{pesquisador.indice_h}</span>
                  </div>
                  <div className="flex flex-col items-center bg-zinc-950 border border-zinc-800 rounded p-2">
                    <span className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-1">Citações</span>
                    <span className="text-xl font-black text-cyan-400">{pesquisador.total_citacoes}</span>
                  </div>
                </div>

                {/* NOVO: Lista de Produções (Artigos) */}
                <div className="mt-auto flex-1 flex flex-col">
                  <h3 className="text-[10px] text-zinc-400 uppercase font-bold tracking-widest mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-600"></span>
                    Principais Produções
                  </h3>
                  
                  {pesquisador.artigos && pesquisador.artigos.length > 0 ? (
                    <ul className="space-y-2 flex-1">
                      {pesquisador.artigos.map((artigo: any, aIndex: number) => (
                        <li key={aIndex} className="bg-zinc-950/80 border border-zinc-800/80 p-2.5 rounded text-xs flex flex-col gap-1.5 hover:border-cyan-800/50 transition-colors">
                          <span className="text-zinc-300 font-medium line-clamp-2 leading-relaxed" title={artigo.titulo}>
                            {artigo.titulo}
                          </span>
                          <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-cyan-900/30 text-cyan-400 w-fit border border-cyan-800/50">
                            QUALIS: {artigo.qualis}
                          </span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-xs text-zinc-600 italic mt-2">Nenhum artigo catalogado.</p>
                  )}
                </div>

              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}