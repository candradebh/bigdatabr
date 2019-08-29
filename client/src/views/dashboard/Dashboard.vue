<template>
  <div class="container">
    <div
      class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom"
    >
      <h1 class="h2">Dashboard</h1>
      <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group mr-2">
          <button type="button" class="btn btn-sm btn-outline-secondary">Compartilhar</button>
          <button type="button" class="btn btn-sm btn-outline-secondary">Exportar</button>
        </div>
        <button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
          <span data-feather="calendar"></span>
          Nessa semana
        </button>
      </div>
    </div>
    <canvas id="chartjs"></canvas>

    <hr />
    <br />
    <h1 class="h2">Modelo de dados</h1>

    <div class="row">
      <div class="col-lg-4">
        <div class="card text-white bg-info mb-3" style="max-width: 18rem;">
          <div class="card-header">Tamanho</div>
          <div class="card-body">
            <h5 class="card-title">{{positivos.length + negativos.length}} tweets</h5>
            <p class="card-text">Tamanho do modelo</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4">
        <div class="card text-white bg-success mb-3" style="max-width: 18rem;">
          <div class="card-header">Positivos</div>
          <div class="card-body">
            <h5 class="card-title">{{positivos.length}} tweets</h5>
            <p
              class="card-text"
            >Indice de acertos é de {{ (this.acertosPositivo*100/this.positivosAvaliados) | numeralFormat }} %</p>
          </div>
        </div>
      </div>
      <div class="col-lg-4">
        <div class="card text-white bg-danger mb-3" style="max-width: 18rem;">
          <div class="card-header">Negativos</div>
          <div class="card-body">
            <h5 class="card-title">{{negativos.length}} tweets</h5>
            <p
              class="card-text"
            >Indice de acertos é de {{ (this.acertosNegativo*100/this.negativosAvaliados) | numeralFormat }} %</p>
          </div>
        </div>
      </div>
    </div>
    <hr>
    <br>
    <div class="row">
      <center>
        <h2>Top Trending Twitter Hashtags</h2>
        <div style="width:700px;height=500px">
          <canvas id="chart"></canvas>
        </div>
      </center>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Chart from "chart.js";
import { Line } from "vue-chartjs";


export default {
  name: 'Dashboard',
  extends: Line,
  data() {
    return {
      negativos: [],
      positivos: [],
      novos: [],
      estatisticas: [],
      indice: [],
      volume: [],
      labels: [],
      chartTrending:'',
      chartDataTrending: '',
      labelsTrending: [],
      valuesTrending: [],
      acertosPositivo: 0,
      positivosAvaliados:0,
      acertosNegativo: 0,
      negativosAvaliados:0,
    };
  },
  created() {


  },
  mounted() {

    this.createChart("chartjs", this.getChartData());
    this.createChartTrending("chart", this.getChartTrending());
    this.getStream();
    this.getTweets();
  },
  methods: {
    createChart(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      const myChart = new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options
      });
    },
    createChartTrending(chartId, chartData) {
      const ctx = document.getElementById(chartId);
      this.chartTrending = new Chart(ctx, {
        type: chartData.type,
        data: chartData.data,
        options: chartData.options
      });
    },
    getStream(){
              setInterval(function(){
                const path = "http://localhost:5000/refreshData";
                axios
                  .get(path)
                  .then(res => {
                    // eslint-disable-next-line
                    this.labelsTrending = res.data.sLabel;
                    this.valuesTrending = res.data.sData;
                  })
                  .catch(error => {
                    // eslint-disable-next-line
                    console.error(error);
                  });

                //this.chartDataTrending.data.labels = this.labelsTrending;
                //this.chartDataTrending.data.datasets[0].data = this.valuesTrending;
                //this.chartTrending.update();

            },1000);
    },
    getTweets() {
      const path = "http://localhost:5000/dashboard";

      axios
        .get(path)
        .then(res => {
          // eslint-disable-next-line
          this.negativos = JSON.parse(res.data.data.tweets_negativos);
          this.positivos = JSON.parse(res.data.data.tweets_positivos);
          this.novos = JSON.parse(res.data.data.tweets_novos);
          this.estatisticas = JSON.parse(res.data.data.tweets_estatisticas);
          for (var i = 0; i < this.estatisticas.length; i++) {
            this.volume.push(this.estatisticas[i].tam_modelo);
            this.indice.push(this.estatisticas[i].indice);
            this.labels.push(this.estatisticas[i].title)
          }

          //indice de acertos
          for (var i = 0; i < this.novos.length; i++) {
            if(this.novos[i].sentimento=='P' ){
              if(this.novos[i].avaliacao!=''){
                this.positivosAvaliados++;
              }
              if(this.novos[i].sentimento == this.novos[i].avaliacao){
                this.acertosPositivo++;
              }
            }
            if(this.novos[i].sentimento=='N' ){
              if(this.novos[i].avaliacao!=''){
                this.negativosAvaliados++;
              }
              if(this.novos[i].sentimento == this.novos[i].avaliacao){
                this.acertosNegativo++;
              }
            }
          }

        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getChartData(){
      let chartData = {
        type: "bar",
        data: {
          labels: this.labels,
          datasets: [
            {
              label: 'Indice de acerto',
              type: 'line', // Add this
              data: this.indice,
              backgroundColor: ["rgba(71, 183,132,.5)"],
              borderColor: ['#36sda'],
              borderWidth: 3
            },
            {
              label: 'Volume do modelo',
              type: 'bar', // Add this
              data: this.volume,
              backgroundColor: ["rgba(54,73,93,.5)"],
              borderColor: ['#36495d'],
              borderWidth: 3
            }
          ],
        },
        options: {
          responsive: true,
          lineTension: 1,
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                  padding: 25
                }
              }
            ]
          }
        }
      };

      return chartData;

    },
    getChartTrending(){

          return {
                type: 'horizontalBar',
                data: {
                    labels: this.labelsTrending,
                    datasets: [{
                        label: '# of Mentions',
                        data: [this.valuesTrending],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
           };
    }
  }
};
</script>
