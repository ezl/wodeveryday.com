<template>
  <div>
    <states-list current_place="country" v-if="countryHasStates"></states-list>
    <cities-list v-else current_place="country"></cities-list>
  </div>
</template>

<script>
  import StatesList from "~/components/StatesList";
  import CitiesList from "~/components/CitiesList";

  export default {
    name: "index",
    components: {
      CitiesList,
      StatesList
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
    computed: {
      countryHasStates() {
        return this.$store.getters.countries_with_countries.indexOf(this.$route.params.country) !== -1
      }
    },

  }
</script>

<style scoped>

</style>
