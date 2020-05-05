<template>
  <v-card style="background: transparent; box-shadow: none;">
    <v-card-text v-if="!gymPhotos" class="text-center">
      <v-progress-circular
        class="mt-5"
        :size="70"
        :width="7"
        color="white"
        indeterminate
      />
    </v-card-text>
    <template>
      <v-img
        v-for="(photo, index) in gymPhotos"
        :key="index"
        :src="photo.getUrl()"
        class="mb-3"
        aspect-ratio="1.7"
      />
    </template>
  </v-card>
</template>

<script>
export default {
  name: "PhotoColumnCard",
  props: {
    gymPhotos: {
      type: Array,
      required: false,
      default: undefined,
    },
  },
}
</script>
