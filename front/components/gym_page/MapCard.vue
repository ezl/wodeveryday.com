<template>
  <v-card class="mb-3">
    <div
      id="map"
      style="height: 500px;"
      class="d-flex justify-center align-center"
    >
      <v-progress-circular
        class="mt-5"
        :size="70"
        :width="7"
        color="white"
        indeterminate
      />
    </div>
    <v-card-text>
      <h3>Located at {{ getGymAddress }}</h3>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "MapCard",
  computed: {
    getGymAddress: function () {
      let gymFullAddress = this.$store.state.gym_object.address
      gymFullAddress += ", " + this.$store.state.gym_object.city
      if (this.$store.state.gym_object.full_state)
        gymFullAddress += ", " + this.$store.state.gym_object.full_state
      gymFullAddress += " " + this.$store.state.gym_object.zip
      return gymFullAddress
    },
  },
}
</script>
