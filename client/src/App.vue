<template>
  <div id="app">
    <search-main></search-main>
    <div class="container-fluid">
      <div class="row">
        <side-menu></side-menu>
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
          <router-view/>
        </main>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
@import "../node_modules/bootstrap/scss/bootstrap.scss";
@import "./assets/styles/custom.scss";
</style>
