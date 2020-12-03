<template>
  <div>
    <h1 class="text-capitalize text-center m-4">
      {{$route.params[current_place]}}
    </h1>
    <cards :items_object="states"></cards>
  </div>
</template>

<script>
  import cards from "./cards";

  export default {
    name: "StatesList",
    components: {cards},
    props: {
      current_place: {
        type: String,
        requiredL: true
      }
    },
    data() {
      return {
        states: {}
      }
    },
    created() {
      this.$nextTick(() => {
        this.$nuxt.$loading.start()
        this.$store.dispatch('getStates', {country: String(this.$route.params.country).replace(/-/gi, ' ')}).then(response => {
          this.states = response

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
