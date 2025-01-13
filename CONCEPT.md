# Fantasy Frontier Concept and High Level Design Document

## Premise

Your homeland has fallen victim to a catastrophe beyond your understanding, but you and a small group were forewarned, allowing you to flee ahead of time. Bringing your small band of followers into the wildlands, to carve out a safe place away from the strife that you had before. Your goal is to found your own city-state, a place of relative safety.

## Design

### Victory Conditions

- Uncertain at this point. Perhaps eliminating some major threat? Multiple possible ways to win?

### Interfaces

- Overland map covering the area around the city
  - This is not randomly-generated, as each map will provide its own challenges, but multiple maps available.
  - Eventually have a map/scenario creator
- City map covering the city to build up facilities.
- Combat Interface(may not be a separate interface)
- Admin interface for unit construction

### Overland tiles

- Some provide bonuses if claimed, like mines and farms
- Distance from the city tile determined maintenance expense and danger of raids, etc.

### City Building

- Hex tiles to build various facilities on.
- These should be districts, like residential and commerce, or mixed, etc.
- Each type of district can house certain upgrades, say a max of 3. Blacksmith, cobbler, tanner, etc.
- Some upgrades take more than one slot, or can be expanded into more than one slot.
- Districts and upgrades can both be upgraded in tier
- Districts provide taxes dependent on wealth level

- Districts include:
  - Commerce (markets, etc)
  - Recreation (parks, squares, etc)
  - Residential
  - Mixed (Residential/Commerce, for shopkeepers living in their shops) - requires research
  - Administrative
  - Military

- Upgrades include these, but some require research:
  - Blacksmith (better equipment available)
  - Fire marshall
  - Guardsmen (police, etc)
  - Library
  - School
  - Mage's Tower
  - Others

### Research

Two trees to research, Tech and Magic.
Dependent on education level, the population randomly produces Thinkers, which boost research level
Thinkers aid Tech, Wizards aid Magic

Sample technologies:

- Architecture: different tiers allow different sub-research or automatic benefits such as
  - Jettying(increases living conditions)
  - Concrete
  - Multi story buildings
- Metallurgy. Upgrades iron to steel and damascus or complex machinery
- Glasswork
- Others such as armor and weapons

Sample Magic benefits:

- Fertility magic: increases crop yields
- Earth magic: Bonuses to stonework etc

### Unit Construction

- Units are built by combining squads.
- Squads made up of archers or infantry, etc
- Different squads have different equipment
- Squads have different abilities. Example: Archers apply one damage strike before combat begins
- Different weaknesses/strengths for units

### Combat

- Still working out how simplified this should be

### Challenges

- Events like storms, floods, etc.
- Raids from hostile tribes (can peace be made?)
- Monster attacks (Adventurer's Guild cuts down on frequency/danger)
