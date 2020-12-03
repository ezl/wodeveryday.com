<template>
  <div class="mt-5">
    <h1 class="text-capitalize text-center m-4">
      {{$route.params[current_place]}}
    </h1>
    <cards :items_object="gyms"></cards>
  </div>
</template>

<script>
  import cards from "./cards";

  export default {
    name: "CitiesList",
    components: {
      cards
    },
    props: {
      current_place: {
        type: String,
        requiredL: true
      }
    },
    data() {
      return {
        gyms: {}
      }
    },
    computed: {
      countryHasStates() {
        return this.$store.getters.countries_with_countries.indexOf(this.$route.params.country) !== -1
      }
    },
    mounted() {
      this.$nextTick(() => {
        this.$nuxt.$loading.start()
        var params = {}
        if (this.countryHasStates) {
          params.state = String(this.$route.params.state).replace(/-/gi, ' ')
        } else {
          params = {
            country: String(this.$route.params.country).replace(/-/gi, ' ')
          }
        }
        this.$store.dispatch('getGyms', params).then(response => {
          this.gyms = response
          this.$nuxt.$loading.finish()
        })

      })
    }
  }
</script>

<style scoped>
  h1 {
    color: var(--brand-color);
  }
</style>
