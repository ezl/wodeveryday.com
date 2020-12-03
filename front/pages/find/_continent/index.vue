<template>
  <div>
<!--    <search></search>-->
    <h1 class="text-capitalize text-center m-4" >
      {{$route.params.continent}}
    </h1>
    <cards :items_object="countries"></cards>
  </div>
</template>

<script>
  import cards from "../../../components/cards";
  import search from "../../../components/search";

  export default {
    name: "index",
    components: {
      cards,
      search
    },
    data() {
      return {
        countries: {}
      }
    },
    created() {
      this.$nextTick(() => {
        this.$nuxt.$loading.start()
        this.$store.dispatch('getCountries', {continent: String(this.$route.params.continent).replace(/-/gi, ' ')}).then(response => {
          this.countries = response
          this.$nuxt.$loading.finish()
        })

      })
    }
  }
</script>

<style scoped>
  h1{
    color: var(--brand-color);
  }
  .card-header {
    color: black;
  }
</style>
