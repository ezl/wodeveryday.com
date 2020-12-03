<template>
<gyms-list :city_name="this.$route.params.city"></gyms-list>
</template>
<script>
  import GymsList from "~/components/GymsList";

  export default {
    name: "index",
    components: {
      GymsList
    }
  }
</script>

<style scoped>

</style>

