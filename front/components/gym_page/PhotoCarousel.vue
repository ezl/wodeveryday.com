<template>
  <v-card id="photoCarousel" class="mb-3">
    <v-card-text v-if="!gymPhotos" class="text-center">
      <v-progress-circular :size="70" :width="7" color="white" indeterminate />
    </v-card-text>
    <v-carousel
      v-if="gymPhotos && gymPhotos.length > 0"
      cycle
      height="600"
      hide-delimiters
    >
      <v-carousel-item v-for="(photo, index) in gymPhotos" :key="index">
        <v-sheet height="100%">
          <v-row class="fill-height" align="center" justify="center">
            <v-img :src="photo.getUrl()" />
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
