<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {computed} from "vue";
import _ from "lodash";
import useMainStore from "stores/mainStore";

const props = defineProps({
  id: {
    required: true,
  }
})

const $q = useQuasar()

const mainStore = useMainStore();

const {
  FORCE_SCRIPT_NAME,
} = storeToRefs(mainStore)

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  statusVerbose,
  comment,
  disabled,
  rpdData,
  admissionData,
  errors,
  lekcHours,
  srsHours,
  prHours,
  labHours,
} = storeToRefs(generatorViewStore)

const menuItems = computed(() => {
  let items = [];
  items.push(...[
      // title (название), url (ссылка), allow (cadmkind, отображать)
      {title: 'Титульный лист', url: 'main', allow: [1, 2, 3, 4, 5]},
      {title: 'Компетенции', url: 'competences', allow: [1, 2, 3, 4]},
      {title: 'Индикаторы', url: 'indicators', allow: [1, 2, 3, 4]},
      {title: 'Результаты освоения программы', url: 'competences', allow: [5]},
      {title: 'Результаты освоения дисциплины ', url: 'indicators', allow: [5]},
      {title: 'Место дисциплины в структуре ООП', url: 'discipline-place', allow: [1, 2, 3, 4]},
      {title: 'Структура дисциплины', url: 'structure', allow: [1, 2, 3, 4, 5]},
    ]
  );

  if (lekcHours.value) {
    items.push({title: 'Содержание лекционных занятий', url: 'discipline-lectures', 'right': true, allow: [1, 2, 3, 4, 5]})
  }
  if (labHours.value) {
    items.push({title: 'Содержание лабораторных работ', url: 'discipline-lab', 'right': true, allow: [1, 2, 3, 4, 5]})
  }
  if (prHours.value) {
    items.push({title: 'Содержание практических занятий', url: 'discipline-practice', 'right': true, allow: [1, 2, 3, 4, 5]})
  }
  if (srsHours.value) {
    items.push( {title: 'Содержание самостоятельных работ', url: 'discipline-independent', 'right': true, allow: [1, 2, 3, 4, 5]})
  }


  items.push(...[
    {title: 'Содержание тем дисциплины', url: 'discipline-theme', allow: [1, 2, 3, 4, 5]},
    {title: 'Перечень учебно-методического обеспечения', url: 'guidelines', allow: [1, 2, 3, 4, 5]},
    {
      title: 'Оценочные материалы по дисциплине для контроля текущей успеваемости',
      url: 'fos',
      allow: [1, 2, 3, 4, 5]
    },
    {title: 'Типовые оценочные средства промежуточной аттестации', url: 'tat', allow: [1, 2, 3, 4, 5]},
    {title: 'Литература', url: 'library', allow: [1, 2, 3, 4, 5]},
    {title: 'Другие ресурсы', url: 'resources', allow: [1, 2, 3, 4, 5]},
    {title: 'Перечень используемых информационных технологий', url: 'soft', allow: [1, 2, 3, 4, 5]},
    {title: 'Материально-техническое обеспечение', url: 'logistics', allow: [1, 2, 3, 4, 5]},
  ]);

  return items;
});

const filterMenuItems = computed(() => {
  return _.filter(menuItems.value, x => x.allow.includes(admissionData.value.cadmkind))
})

const criticalErrors = computed(() => {
  return _.filter(errors.value, x => x.level == 'critical')
})

async function sendToReview() {
  $q.loading.show()
  let r = await api.get(`/api/generator/${activeRpdId.value}/send-rpd-on-review/`)
  rpdData.value.status = r.data.status
  rpdData.value.status_verbose = r.data.status_verbose
  $q.loading.hide()
}

function translateDate(date) {
  let result = new Date(date).toLocaleString('ru')
  return result
}

function getErrors(url) {
  return _.filter(errors.value, x => x.url == url)
}


</script>

<template>
  <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden; height: 100%">
    <div class="q-pa-sm">
      <div class="bg-pink-3 rounded-borders" v-if="comment.length != 0">
        <div class="text-subtitle1">{{ comment.user__last_name }} {{ comment.user__first_name }} оставил комментарий
        </div>
        <div>
          <div class="q-ma-xs text-subtitle2">
            <div>
              <div class="text-subtitle1 text-bold">{{ translateDate(comment.created_at) }}</div>
              <div>
                {{ comment.comment }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!disabled" class="q-mb-sm">
        <q-btn
          class="q-mt-xs"
          color="secondary"
          dense
          @click="sendToReview"
          style="width: 100%"
          label="Отправить на согласование"
          :disabled="criticalErrors.length != 0"
        />
      </div>
      <div v-else class="text-center q-mb-md">
        <q-btn
          class="q-mt-xs"
          color="secondary"
          dense
          disable
          style="width: 100%"
          :label="statusVerbose"
        />
      </div>
    </div>
    <q-list
      style="overflow-y: auto"
      bordered
      separator
    >
      <q-item
        v-for="item in filterMenuItems"
        clickable
        v-ripple
        active-class="bg-amber-2 text-black"
        :to="`/generator/${id}/${item.url}`"
        dense
        style="padding: 12px;"
      >
        <q-item-section>
          <q-item-label :class="item.right ? 'q-ml-lg' : ''">{{ item.title }}</q-item-label>
          <!--        <q-item-label caption>Основная информация о программе</q-item-label>-->
        </q-item-section>
        <q-item-section avatar v-if="getErrors(item.url).length != 0">
          <q-icon :name="getErrors(item.url)[0].level == 'warning' ? 'mdi-alert' : 'mdi-alert-box'"
                  :color="getErrors(item.url)[0].level == 'warning' ? 'amber-4' : 'red-7'">
            <q-tooltip class="text-white hide-scrollbar"
                       :class="getErrors(item.url)[0].level == 'warning' ? 'bg-amber-8' : 'bg-red-9'" max-height="20%">
              <div v-for="error in getErrors(item.url)" style="font-size: 14px;">
                <div v-for="text in error.text">
                  {{ text }}
                </div>
              </div>
            </q-tooltip>
          </q-icon>
        </q-item-section>
      </q-item>

    </q-list>

  </div>
</template>

<style scoped>

</style>
