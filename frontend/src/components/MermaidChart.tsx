import { useEffect, useId, useState } from "react";
import mermaid from "mermaid";

mermaid.initialize({
  startOnLoad: false,
  theme: "neutral", // 'default', 'neutral', 'dark', 'forest'
  securityLevel: "loose",
  fontFamily: "sans-serif",
});

interface MermaidChartProps {
  chart: string;
}

export const MermaidChart = ({ chart }: MermaidChartProps) => {
  const id = useId().replace(/:/g, "");
  const [svg, setSvg] = useState("");

  useEffect(() => {
    const renderChart = async () => {
      try {
        const { svg } = await mermaid.render(`mermaid-${id}`, chart);
        setSvg(svg);
      } catch (error) {
        console.error("Failed to render mermaid chart:", error);
        setSvg(
          `<div style="color:red; padding:10px; border:1px solid red;">Failed to render diagram</div>`,
        );
      }
    };

    if (chart) {
      renderChart();
    }
  }, [chart, id]);
  return (
    <div
      className="flex justify-center p-6 my-4 bg-white border rounded-lg shadow-sm border-slate-100 overflow-x-auto"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
};
