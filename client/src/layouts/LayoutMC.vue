<script setup lang="ts">

</script>

<template>
  <div class="panel-container">
    <div class="q-pa-sm left-menu">
      <slot name="left-menu"></slot>
    </div>
    <div class="content">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.panel-container {
  display: grid;
  grid-template-columns: 20% auto;
  grid-template-areas: "m c";
  height: 100%;
  position: absolute; left: 0; right: 0; top: 0; bottom: 0; overflow: hidden;
}

.left-menu {
  grid-area: m;
  border-right: 1px solid silver;
  box-shadow: 0 0 8px silver;
  overflow: hidden;
}

.content {
  grid-area: c;
  padding: 16px;
  overflow: hidden;
}

</style>
