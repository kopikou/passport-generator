<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {onBeforeMount, ref, watch} from "vue";
import _, {forEach} from "lodash";
import {api} from "boot/axios";
import {laObjectGroup} from "@quasar/extras/line-awesome";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  fosInfo,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  }
})

const $q = useQuasar()
const about = ref('')
const criteria = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  _.set(fosInfo.value, `[0].${props.type}`, {
    "about": about.value,
    "criteria": criteria.value,
    "title": props.title,
  })
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": "fos",
    "value": fosInfo.value,
  })
  $q.loading.hide()
}

watch(additionalInfo, () => {
  about.value = _.get(fosInfo.value, `[0].${props.type}.about`)
  criteria.value = _.get(fosInfo.value, `[0].${props.type}.criteria`)
})

onBeforeMount(() => {
  about.value = _.get(fosInfo.value, `[0].${props.type}.about`)
  criteria.value = _.get(fosInfo.value, `[0].${props.type}.criteria`)
})

</script>

<template>
  <q-expansion-item
    :label=props.title
  >
    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
          />
          <q-input
            label="Критерии оценивания"
            type="textarea"
            filled
            stack-label
            v-model="criteria"
          />
          <q-btn
            label="Сохранить"
            color="primary"
            @click="saveData"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
