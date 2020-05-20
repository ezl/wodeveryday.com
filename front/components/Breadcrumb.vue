<template>
  <v-card-text>
    <h3
      v-for="(name, index) in breadcrumbNames"
      :key="index"
      class="text-uppercase d-inline-block"
    >
      <nuxt-link :to="breadcrumbPaths[index] || ''">
        <v-btn text>
          {{ name }}
        </v-btn>
      </nuxt-link>
      <span v-if="index != breadcrumbNames.length - 1" class="px-2">
        >
      </span>
    </h3>
  </v-card-text>
</template>

<script>
export default {
  name: "Breadcrumb",
  props: {
    breadcrumbNames: {
      type: Array,
      required: true,
      default: Array,
    },
    breadcrumbPaths: {
      type: Array,
      default: Array,
    },
  },
}
</script>
