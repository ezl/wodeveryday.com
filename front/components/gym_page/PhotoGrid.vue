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
      <div class="text-center">
        <v-dialog
          v-model="dialog"
          fullscreen
          transition="dialog-bottom-transition"
        >
          <v-card>
            <v-card-title class="headline grey lighten-2">
              {{ fetchPhotoAltTag }}
            </v-card-title>

            <v-card-text>
              <v-img
                v-if="d_data"
                :src="d_data.photo_url"
                aspect-ratio="1.7"
                max-height="85vh"
                contain
                :alt="fetchPhotoAltTag"
              />
            </v-card-text>

            <v-divider />

            <v-card-actions>
              <v-spacer />
              <v-btn color="primary" text @click="dialog = false">
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
      <v-row>
        <v-col v-for="(photo, index) in gymPhotos" :key="index" cols="4">
          <v-img
            :id="'btn_img_' + index"
            :src="photo.photo_url"
            class="mb-3"
            aspect-ratio="1.7"
            contain
            max-height="300"
            :alt="fetchPhotoAltTag"
            @click="
              dialog = true
              d_data = photo
            "
          />
        </v-col>
      </v-row>
    </template>
  </v-card>
</template>

<script>
export default {
  name: "PhotoGrid",
  data: function () {
    return {
      dialog: false,
      d_data: null,
    }
  },
  computed: {
    gymPhotos: function () {
      if (this.$store.state.place_details.photos) {
        return this.$store.state.place_details.photos.slice(0, 9)
      }
      if (this.$store.state.place_photos.photos) {
        return this.$store.state.place_photos.photos.slice(0, 9)
      }
      return []
    },
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
