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

    <canvas ref="chart"></canvas>

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
                <td>{{ moment(positivo.tweet.created_at).format("DD/MM/YYYY") }}</td>
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
                <td>{{ moment(negativo.tweet.created_at).format("DD/MM/YYYY") }}</td>
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
              <td>{{ moment(novo.tweet.created_at).format("DD/MM/YYYY") }}</td>
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

export default {
  name: "Dashboard",
  data() {
    return {
      negativos: "",
      positivos: "",
      novos: "",
      estatisticas:[],
      indice:[],
      volume:[],
      chartData: {
        labels: [
          "100",
          "200",
          "300",
          "400",
        ],
        datasets: [

        ]
      },
    };
  },
  created() {




  },
  mounted() {
    this.getTweets();

    this.chartData.datasets.push({
            type: "line",
            label: "Indice de acertos",
            borderColor: "rgb(54, 162, 235)",
            borderWidth: 2,
            fill: false,
            data: this.indice
          });
    this.chartData.datasets.push({
            type: "line",
            label: "Volume",
            backgroundColor: "rgb(255, 99, 132)",
            data: this.volume,
            borderColor: "white",
            borderWidth: 2
          });

    var chart = this.$refs.chart;
    var ctx = chart.getContext("2d");

    var config = new Chart(ctx, {
      type: "bar",
      data: this.chartData,
      options: {
        responsive: true,
        title: {
          display: true,
          text: "Volume do Modelo de Treino x Eficiência do Algoritimo"
        },
        tooltips: {
          mode: "index",
          intersect: true
        }
      }
    });

    var myChart = new Chart(ctx, config);
  },
  methods: {


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
          for(var i=0;i<this.estatisticas.length;i++){
            this.volume.push(this.estatisticas[i].tam_modelo);
            this.indice.push(this.estatisticas[i].indice);
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  }
};
</script>
