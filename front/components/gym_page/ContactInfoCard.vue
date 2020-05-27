<template>
  <v-card class="pb-2">
    <v-card-text>
      <h3>Contact Info</h3>
    </v-card-text>
    <v-divider />
    <v-btn large class="ma-2" :href="gymWebsite" target="_blank">
      Visit their website
    </v-btn>
    <v-tooltip v-if="phoneNumberVisible" right>
      <template v-slot:activator="{ on }">
        <v-btn
          id="phone_field"
          large
          class="ml-2 d-block"
          :loading="gymPhoneNumber === undefined"
          v-on="on"
          @click="copyToClipboard()"
        >
          {{ gymPhoneNumber
          }}<v-icon right>
            mdi-content-copy
          </v-icon>
        </v-btn>
      </template>
      <span>Click to copy</span>
    </v-tooltip>
    <v-tooltip v-if="$store.state.current_affiliate.email" right>
      <template v-slot:activator="{ on }">
        <v-btn
          id="phone_field"
          large
          class="ml-2 d-block"
          v-on="on"
          @click="copyToClipboard()"
        >
          {{ $store.state.current_affiliate.email
          }}<v-icon right>
            mdi-content-copy
          </v-icon>
        </v-btn>
      </template>
      <span>Click to copy</span>
    </v-tooltip>
  </v-card>
</template>

<script>
export default {
  name: "ContactInfoCard",
  props: {
    gymWebsite: {
      type: String,
      required: false,
      default: undefined,
    },
    gymPhoneNumber: {
      type: String,
      required: false,
      default: undefined,
    },
  },
  computed: {
    phoneNumberVisible: function () {
      return (
        this.gymPhoneNumber === undefined ||
        (this.gymPhoneNumber && this.gymPhoneNumber.length > 0)
      )
    },
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.gymPhoneNumber)
    },
  },
}
</script>
