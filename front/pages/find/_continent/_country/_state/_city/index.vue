<template>
<gyms-list :city_name="this.$route.params.city"></gyms-list>
</template>
<script>
  import GymsList from "~/components/GymsList";

  export default {
    name: "index",
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
    components: {
      GymsList
    }
  }
</script>

<style scoped>

</style>

