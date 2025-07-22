<script setup lang="ts">
import LayoutHCF from "components/LayoutHCF.vue";
import {ref} from "vue";
import {LocalStorage} from "quasar";
import {Admission} from "src/types";

const textFilter = ref<String>(LocalStorage.getItem('surp_rop_direction_filter') || '');
const admissions = ref<Admission[]>([]);


</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: center;">
          <q-input outlined label="Поиск по направлению или РОПу"
                   v-model="textFilter" clearable/>
          <q-btn
              icon="mdi-abacus"
              color="green-6"
              size="md"
              label="Рассчитать"
              target="_blank"
              @click="getDoneFile('rpd')"
          />
        </div>
      </div>
    </template>
    <template #content>

    </template>
  </layout-h-c-f>
</template>

<style scoped>

</style>
