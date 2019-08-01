<template>
  <div class="container">
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
