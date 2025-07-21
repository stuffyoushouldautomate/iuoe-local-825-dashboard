import React from 'react';
import Plot from 'react-plotly.js';

interface ChartProps {
  type: 'line' | 'bar' | 'pie';
  data: any[];
  title: string;
}

const Chart: React.FC<ChartProps> = ({ type, data, title }) => {
  // Placeholder chart data - will be replaced with real data
  const placeholderData = {
    line: [
      {
        x: ['2020', '2021', '2022', '2023', '2024'],
        y: [145000, 148000, 152000, 155000, 158000],
        type: 'scatter',
        mode: 'lines+markers',
        name: 'NJ Construction Employment',
        line: { color: '#3b82f6', width: 3 },
        marker: { size: 8 }
      }
    ],
    bar: [
      {
        x: ['Earlco', 'Boyce', 'NJ DOT', 'Bergen Co', 'Essex Co'],
        y: [12.5, 8.9, 45.0, 22.0, 18.0],
        type: 'bar',
        name: 'Contract Value ($M)',
        marker: { color: '#10b981' }
      }
    ],
    pie: [
      {
        values: [35, 25, 20, 20],
        labels: ['Heavy Construction', 'Building Construction', 'Specialty Trades', 'Infrastructure'],
        type: 'pie',
        name: 'Construction Types'
      }
    ]
  };

  const layout = {
    title: title,
    autosize: true,
    margin: { l: 50, r: 50, t: 50, b: 50 },
    font: { family: 'Inter, sans-serif' },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
    xaxis: {
      showgrid: true,
      gridcolor: '#e5e7eb',
      zeroline: false
    },
    yaxis: {
      showgrid: true,
      gridcolor: '#e5e7eb',
      zeroline: false
    }
  };

  const config = {
    displayModeBar: false,
    responsive: true
  };

  return (
    <div className="w-full h-64">
      <Plot
        data={data.length > 0 ? data : placeholderData[type]}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    </div>
  );
};

export default Chart; 