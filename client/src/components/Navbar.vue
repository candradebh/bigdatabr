<template>
  <nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link :to="{ name: 'Dashboard' }" class="nav-link" active-class="active" exact >
            Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link :to="{ name: 'Coleta' }" class="nav-link" active-class="active" >
             Treinar Modelo
          </router-link>
        </li>
        <li class="nav-item">
         <router-link :to="{ name: 'Treinamento' }" class="nav-link" active-class="active" >
             Buscar novos
          </router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="bar-chart-2"></span>
            Reports
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="layers"></span>
            Integrations
          </a>
        </li>
      </ul>

      <h6 class="sidebar-heading d-flex justify-content-between
                align-items-center px-3 mt-4 mb-1 text-muted" >
        <span>Saved reports</span>
        <a class="d-flex align-items-center text-muted" href="#">
          <span data-feather="plus-circle"></span>
        </a>
      </h6>
      <ul class="nav flex-column mb-2">
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="file-text"></span>
            Current month
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="file-text"></span>
            Last quarter
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="file-text"></span>
            Social engagement
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="file-text"></span>
            Year-end sale
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
export default {
  name: 'Navbar',
};
</script>
