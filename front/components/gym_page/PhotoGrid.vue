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
    <template v-if="gymPhotos && gymPhotos.length > 0">
      <v-row>
        <v-col v-for="(photo, index) in gymPhotos" :key="index" cols="4">
          <v-img
            :src="photo.getUrl()"
            class="mb-3"
            aspect-ratio="1.7"
            :alt="fetchPhotoAltTag"
          />
        </v-col>
      </v-row>
    </template>
  </v-card>
</template>

<script>
export default {
  name: "PhotoGrid",
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
