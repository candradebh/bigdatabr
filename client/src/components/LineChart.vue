<template>

</template>
<script>
import { Line } from 'vue-chartjs';

export default {
  name: 'Navbar',
  props: ['datasets', 'config'],
  extends: Line,
  mounted() {
    this.renderChart({
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        this.datasets,
      ],
    }, this.config);
  },

};
</script>
