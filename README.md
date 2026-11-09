# Team Work Source

The employee blueprints and task blueprints that come with [Team Work](https://github.com/yanun0323/Team-Work).
Team Work reads this repo as its official source and keeps it up to date by itself.

- `blueprints/` – one employee blueprint per file
- `workflows/` – one task blueprint per file
- `skills/` – skills the blueprints read, one folder with a `SKILL.md` each

A file's name becomes part of the blueprint's id (`team-work--<name>`), so renaming a file makes it a different
blueprint: employees working by the old one keep it as their own settings.

## Where skills come from

A blueprint's `skills` lists where its employees find skills, read in that order; when two have a skill of the same
name, the first one read wins.

```yaml
skills:
  - path: ~/.agents/            # a folder on the user's computer
  - path: skills                # a folder in this repo
  - repo: https://github.com/anthropics/skills
    ref: main
    path: skills                # optional: a folder in that repo
    include: [docx, pdf]        # optional: only these skills; exclude leaves some out
```

## Writing in several languages

`name`, `prompt` and `comment` of a blueprint, and `name` and `prompt` of a flow and of its steps, take either one
text or a text for each language Team Work shows: `en`, `zh`, `zh-Hans`, `ja`, `ko`.

```yaml
name:
  en: Generalist
  zh: 通才
prompt:
  en: |-
    You are the company's generalist...
  zh: |-
    你是這間公司的通才……
```

The app shows the language the user picked, then English, then the first one written. Employees are given the
English text when there is one.
