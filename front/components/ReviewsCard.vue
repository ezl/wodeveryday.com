<template>
  <v-card>
    <v-card-text v-if="!gymReviews" class="text-center">
      <v-progress-circular :size="70" :width="7" color="white" indeterminate />
    </v-card-text>
    <template v-if="gymReviews && gymReviews.length > 0">
      <v-card-text>
        <h3>{{ gymName }} Reviews</h3>
      </v-card-text>
      <v-list three-line>
        <template v-for="(review, index) in gymReviews">
          <v-divider :key="index" />
          <v-list-item :key="review.author_name">
            <v-list-item-avatar>
              <v-img :src="review.profile_photo_url" />
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ review.author_name }}</v-list-item-title>
              <v-card-actions class="pl-0">
                <v-rating
                  v-model="review.rating"
                  readonly
                  background-color="yellow"
                  color="yellow accent-4"
                  dense
                  size="18"
                />
                <span class="grey--text text--lighten-2 caption mr-2">
                  ({{ review.relative_time_description }})
                </span>
              </v-card-actions>
              <v-list-item-subtitle>{{ review.text }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </template>
  </v-card>
</template>

<script>
export default {
  name: "ReviewsCard",
  props: {
    gymReviews: {
      type: Array,
      required: false,
      default: undefined,
    },
    gymName: {
      type: String,
      required: false,
      default: undefined,
    },
  },
}
</script>
