<template>
  <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">IGTI</a>
      <input
        class="form-control form-control-dark w-100"
        type="text"
        placeholder="Pesquisar"
        aria-label="Pesquisar"
      >
      <ul class="navbar-nav px-3">
        <li class="nav-item text-nowrap">
          <a class="nav-link" href="#">Sair</a>
        </li>
      </ul>
    </nav>
</template>
<script>
export default {
  name: 'SearchMain',
};
</script>
