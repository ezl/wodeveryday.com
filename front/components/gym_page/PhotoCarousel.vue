<template>
  <v-card id="photoCarousel" class="mb-3">
    <v-card-text v-if="!gymPhotos" class="text-center">
      <v-progress-circular :size="70" :width="7" color="white" indeterminate />
    </v-card-text>
    <v-carousel
      v-if="gymPhotos && gymPhotos.length > 0"
      height="600"
      hide-delimiters
    >
      <v-carousel-item v-for="(photo, index) in gymPhotos" :key="index">
        <v-sheet height="100%">
          <v-row class="fill-height" align="center" justify="center">
            <v-img :src="photo.getUrl()" :alt="fetchPhotoAltTag" />
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
  </v-card>
</template>

<script>
export default {
  name: "PhotoCarousel",
  props: {
    gymPhotos: {
      type: Array,
      required: false,
      default: undefined,
    },
  },
  computed: {
    fetchPhotoAltTag: function () {
      let altTag = `Photo of ${this.$store.state.gym_object.name} in ${this.$store.state.gym_object.city}, `

      if (this.$store.state.gym_object.full_state)
        altTag += `${this.$store.state.gym_object.full_state}, `

      altTag += `${this.$store.state.gym_object.country}`

      return altTag
    },
  },
}
</script>

<style lang="scss" scoped>
#photoCarousel {
  display: none;
  @media (max-width: 960px) {
    display: block;
  }
}
</style>
