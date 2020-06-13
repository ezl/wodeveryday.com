<template>
  <v-app dark>
    <v-content>
      <nuxt />
    </v-content>
    <gym-footer />
  </v-app>
</template>

<script>
import GymFooter from "~/components/global/GymFooter.vue"

export default {
  components: {
    GymFooter,
  },
}
</script>
