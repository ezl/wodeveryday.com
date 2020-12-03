<template>
  <div>
<!--    <search></search>-->
    <states-list current_place="country" v-if="countryHasStates"></states-list>
    <cities-list v-else current_place="country"></cities-list>
  </div>
</template>

<script>
  import StatesList from "~/components/StatesList";
  import CitiesList from "~/components/CitiesList";
  import search from "../../../../components/search";

  export default {
    name: "index",
    components: {
      CitiesList,
      search,
      StatesList
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
