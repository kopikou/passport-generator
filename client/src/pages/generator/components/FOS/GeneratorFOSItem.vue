<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {computed, nextTick, onBeforeMount, ref, watch, watchEffect} from "vue";
import _, {forEach} from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  fosInfo,
  disabled,
  disciplineThemes,
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

const themes = computed(() => {
  return _.filter(disciplineThemes.value, x => x.formcontrol_list.includes(props.type))
})

async function saveData() {
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  fosInfo.value = [...((fosInfo.value || []).filter((x: any) => x.type != props.type)), {
    "about": about.value,
    "criteria": criteria.value,
    "title": props.title,
    "type": props.type,
  }];

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": "fos",
    "value": fosInfo.value,
  })

  //   if (r.status == 200) {
  $q.notify({
    message: "Данные <span class='text-bold'>о фонде оценочных средств дисциплине</span> сохранены!",
    color: "secondary",
    position: "bottom-right",
    html: true,
  })
  await generatorViewStore.getData()
  generatorViewStore.checkErrors()
  //   } else {
  //     $q.notify({
  //       message: "Данные <span class='text-bold'>о фонде оценочных средств дисциплине</span> не сохранены!",
  //       color: "negative",
  //       position: "bottom",
  //       html: true,
  //     })
  //   }
  // })
  //
  // const key = _.findKey(fosInfo.value || [], x => x.type == props.type)
  // if (!key) {
  //   fosInfo.value.push({
  //     "about": about.value,
  //     "criteria": criteria.value,
  //     "title": props.title,
  //     "type": props.type,
  //   })
  // } else {
  //   _.set(fosInfo.value, `[${key}]`, {
  //     "about": about.value,
  //     "criteria": criteria.value,
  //     "title": props.title,
  //     "type": props.type,
  //   })
  // }


// $q.loading.hide()
}

watchEffect(() => {
  const key = _.findKey(fosInfo.value, x => x.type == props.type)
  if (key) {
    about.value = _.get(_.find(fosInfo.value, x => x.type == props.type), 'about', '')
    criteria.value = _.get(_.find(fosInfo.value, x => x.type == props.type), 'criteria', '')
  }
})

</script>

<template>
  <q-expansion-item v-bind="$attrs">

    <template #header>
      <q-item-section>
        {{ props.title }}
        <div>
          <q-chip
            v-for="theme in _.sortBy(themes, x => [x.semester, x.num])"
            :label="`${theme.semester}-${theme.num}. ${theme.name}`"
            style="max-width: 400px"
          >
            <q-tooltip>{{ theme.name }}</q-tooltip>
          </q-chip>
        </div>
      </q-item-section>
    </template>

    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
          <q-input
            label="Критерии оценивания"
            type="textarea"
            filled
            stack-label
            v-model="criteria"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
          <!--          <q-btn-->
          <!--            label="Сохранить"-->
          <!--            color="primary"-->
          <!--            @click="saveData"-->
          <!--            v-show="!disabled"-->
          <!--          />-->
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
