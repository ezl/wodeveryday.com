<template>
  <div>
<!--    <search></search>-->

    <cities-list v-if="countryHasStates" current_place="state"></cities-list>
    <gyms-list :city_name="$route.params.state" v-else></gyms-list>
  </div>
</template>

<script>
  import CitiesList from "~/components/CitiesList";
  import GymsList from "~/components/GymsList";
  import search from "../../../../../components/search";

  export default {
    name: "index",
    components: {
      CitiesList,
      search,
      GymsList,
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
