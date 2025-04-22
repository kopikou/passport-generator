<script setup lang="ts">
import LayoutHCF from "components/LayoutHCF.vue";

const props = defineProps({
  title: String,
  comment: String,
})

</script>

<template>
  <div class="layout-wrapper">
    <div class="layout-wrapper-header" >
      <div class="q-px-md">
        <div style="display:flex; justify-content: space-between; margin-bottom: 0.5rem">
          <div class="q-mb-sm" style="font-size: 1.25rem">{{ title }}</div>
          <slot name="title-right"></slot>
        </div>
        <slot name="header">
        </slot>
      </div>
    </div>

    <div class="layout-wrapper-content">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<style scoped>
.layout-wrapper {
  display: grid;
  grid-template-rows:  auto 1fr;
  overflow: hidden;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  position: absolute;
  align-items: start;
}

.layout-wrapper-header {
  padding-top: 0.5rem;
  background: v-bind('background');
  border-bottom: 1px solid silver;
  width: 100%;
  overflow: hidden;
  z-index: 100;
}

.layout-wrapper-content {
  overflow-y: auto;
  align-content: start;
  height: 100%;
}
</style>
