<template>
  <div>
    <cities-list v-if="countryHasStates" current_place="state"></cities-list>
    <gyms-list :city_name="$route.params.state" v-else></gyms-list>
  </div>
</template>

<script>
  import CitiesList from "~/components/CitiesList";
  import GymsList from "~/components/GymsList";

  export default {
    name: "index",
    components: {
      CitiesList,
      GymsList,
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
