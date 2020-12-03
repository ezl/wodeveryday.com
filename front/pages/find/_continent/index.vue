<template>
  <div>
    <h1 class="text-capitalize text-center m-4" >
      {{$route.params.continent}}
    </h1>
    <cards :items_object="countries"></cards>
  </div>
</template>

<script>
  import cards from "../../../components/cards";

  export default {
    name: "index",
    components: {
      cards,
    },
    head() {
      return {
        title: 'wodeveryday',
        meta: [
          // hid is used as unique identifier. Do not use `vmid` for it as it will not work
          // {
          //   hid: 'description',
          //   name: 'description',
          //   content: 'My custom description'
          // }
        ]
      }
    },
    data() {
      return {
        countries: {}
      }
    },
    mounted() {
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
