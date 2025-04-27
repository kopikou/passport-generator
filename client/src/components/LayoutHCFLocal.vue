<script setup lang="ts">

</script>

<template>
  <div class="layout-wrapper">
    <div class="layout-wrapper-header">
      <slot name="header"></slot>
    </div>

    <div class="layout-wrapper-content">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
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
  padding-top: 1rem;
  background: $grey-3;
  box-shadow: 0 4px 8px silver;
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
