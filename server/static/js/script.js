const ctx = document.getElementById('inflChart').getContext('2d');
let chart = new Chart(ctx, {
  type: 'line',
  data: { labels: [], datasets: [] },
  options: {
    responsive: true,
    plugins: { 
      legend: { 
        labels: { color: '#e2e8f0' } 
      } 
    },
    scales: {
      x: { 
        ticks: { color: '#94a3b8' },
        title: { display: true, text: 'Jahr', color: '#e2e8f0' }
      },
      y: { 
        ticks: { color: '#94a3b8' },
        title: { display: true, text: 'Inflation (%)', color: '#e2e8f0' }
      }
    }
  }
});

document.getElementById('loadBtn').addEventListener('click', async () => {
  try {
    const res = await fetch('/api/predictions');
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    
    const data = await res.json();

    // Debug-Ausgabe
    console.log("Empfangene Daten:", data);

    const years = data.map(d => d.Year);
    const actual = data.map(d => d.Actual);
    const pred = data.map(d => d.Prediction);

    chart.data.labels = years;
    chart.data.datasets = [
      {
        label: 'Tatsächliche Inflation',
        data: actual,
        borderColor: 'rgba(6,182,212,1)',
        backgroundColor: 'rgba(6,182,212,0.2)',
        borderWidth: 2,
        tension: 0.3,
        fill: true,          
        spanGaps: false
      },
      {
        label: 'Vorhersage',
        data: pred,
        borderColor: 'rgba(239,68,68,1)',
        backgroundColor: 'rgba(239,68,68,0.2)',
        borderWidth: 2,
        borderDash: [6, 3],
        tension: 0.3,
        fill: true,          
        spanGaps: false
      }
    ];

    chart.update();
  } catch (error) {
    console.error("Fehler beim Laden der Daten:", error);
    alert("Daten konnten nicht geladen werden. Siehe Konsole für Details.");
  }
});