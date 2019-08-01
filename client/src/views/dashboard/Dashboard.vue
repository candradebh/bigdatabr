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

    <div class="row">
      <div class="col-md-6">
        <h2>Positivos</h2>
        <div class="table-responsive">
          <table class="table table-striped table-sm">
            <thead>
              <tr>
                <th>Data</th>
                <th>Texto</th>
                <th>Usuário</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="positivo in positivos" :key="positivo.id">
                <td>{{ moment(positivo.tweet.created_at).format('DD/MM/YYYY') }}</td>
                <td>{{ positivo.text}}</td>
                <td>{{ positivo.tweet.user.name}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col-md-6">
        <h2>Negativos</h2>
        <div class="table-responsive">
          <table class="table table-striped table-sm">
            <thead>
              <tr>
                <th>Data</th>
                <th>Texto</th>
                <th>Usuário</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="negativo in negativos" :key="negativo.id">
                <td>{{ moment(negativo.tweet.created_at).format('DD/MM/YYYY') }}</td>
                <td>{{ negativo.text}}</td>
                <td>{{ negativo.tweet.user.name}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="row">
      <h2>Buscados e Classificados Automaticamente</h2>
      <div class="table-responsive">
        <table class="table table-striped table-sm">
          <thead>
            <tr>
              <th>Data</th>
              <th>Texto</th>
              <th>Usuário</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="novo in novos" :key="novo.id">
              <td>{{ moment(novo.tweet.created_at).format('DD/MM/YYYY') }}</td>
              <td>{{ novo.text}}</td>
              <td>{{ novo.tweet.user.name}}</td>
            </tr>
          </tbody>
        </table>
      </div>
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

    };
  },
  created() {
    this.getTweets();

  },
  mounted() {
    this.createChart("chartjs", this.getChartData());
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

    }
  }
};
</script>
