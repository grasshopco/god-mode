-- ===============================================================
-- TABLE SCHEMA DOCUMENTATION: [TABLE_NAME]
-- ===============================================================

/*
  OVERVIEW
  --------
  [DETAILED_TABLE_DESCRIPTION]
  
  This table [EXPLAIN_TABLE_PURPOSE_AND_FUNCTION].
  
  [ADDITIONAL_CONTEXT_ABOUT_THE_TABLE] (optional)
  
  [EXPLAIN_HOW_THIS_TABLE_RELATES_TO_OTHER_TABLES] (optional)
*/

-- 1. DESIGN PRINCIPLES & PHILOSOPHY
-- --------------------------------
/*
  This table design is guided by the following principles:

  1. [DESIGN_PRINCIPLE_1]: [EXPLAIN_DESIGN_PRINCIPLE_1]
  2. [DESIGN_PRINCIPLE_2]: [EXPLAIN_DESIGN_PRINCIPLE_2]
  3. [DESIGN_PRINCIPLE_3]: [EXPLAIN_DESIGN_PRINCIPLE_3]

  These principles align with the system's broader architectural goals of [DESCRIBE_ARCHITECTURAL_GOALS].
*/

-- 2. KEY DESIGN DECISIONS
-- ----------------------
/*
  1. [DECISION_1]: [EXPLAIN_DECISION_1_AND_RATIONALE]
  2. [DECISION_2]: [EXPLAIN_DECISION_2_AND_RATIONALE]
  3. [DECISION_3]: [EXPLAIN_DECISION_3_AND_RATIONALE]
*/

-- 3. SCHEMA DEFINITION
-- -------------------
CREATE TABLE public.[TABLE_NAME] (
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS],                -- [INLINE_COMMENT]
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS],                -- [INLINE_COMMENT]
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS],                -- [INLINE_COMMENT]
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS] DEFAULT '{
    "[JSONB_PROPERTY_1]": [JSONB_DEFAULT_VALUE_1],              -- [JSONB_PROPERTY_1_DESCRIPTION]
    "[JSONB_PROPERTY_2]": [JSONB_DEFAULT_VALUE_2],              -- [JSONB_PROPERTY_2_DESCRIPTION]
    "[JSONB_PROPERTY_3]": {                                     -- [JSONB_PROPERTY_3_DESCRIPTION]
      "[NESTED_PROPERTY_1]": [NESTED_DEFAULT_VALUE_1],          -- [NESTED_PROPERTY_1_DESCRIPTION]
      "[NESTED_PROPERTY_2]": [NESTED_DEFAULT_VALUE_2]           -- [NESTED_PROPERTY_2_DESCRIPTION]
    },
    "[JSONB_PROPERTY_4]": [                                     -- [JSONB_PROPERTY_4_DESCRIPTION]
      {
        "[ARRAY_ITEM_PROPERTY_1]": [ARRAY_ITEM_VALUE_1],        -- [ARRAY_ITEM_PROPERTY_1_DESCRIPTION]
        "[ARRAY_ITEM_PROPERTY_2]": [ARRAY_ITEM_VALUE_2]         -- [ARRAY_ITEM_PROPERTY_2_DESCRIPTION]
      }
    ]
  }'::jsonb,                                                    -- [JSONB_FIELD_DESCRIPTION]
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS] DEFAULT NOW(),  -- [INLINE_COMMENT]
  [FIELD_NAME] [FIELD_TYPE] [FIELD_CONSTRAINTS]                 -- [INLINE_COMMENT]
);

-- 4. INDEXES & CONSTRAINTS
-- -----------------------
-- Indexes
CREATE INDEX idx_[TABLE_NAME]_[FIELD_NAME] ON public.[TABLE_NAME]([FIELD_NAME]);
CREATE INDEX idx_[TABLE_NAME]_[FIELD_NAME]_[FIELD_NAME] ON public.[TABLE_NAME]([FIELD_NAME], [FIELD_NAME]);
CREATE INDEX idx_[TABLE_NAME]_[JSONB_FIELD_NAME] ON public.[TABLE_NAME](([JSONB_FIELD_NAME]->>'[JSONB_KEY]'));

-- Constraints (optional)
ALTER TABLE public.[TABLE_NAME] ADD CONSTRAINT fk_[TABLE_NAME]_[FIELD_NAME] FOREIGN KEY ([FIELD_NAME]) REFERENCES public.[REFERENCED_TABLE]([REFERENCED_FIELD]);
CREATE UNIQUE INDEX idx_[TABLE_NAME]_unique_[FIELD_NAME] ON public.[TABLE_NAME]([FIELD_NAME]) WHERE [CONDITION];

-- 5. COMMENTS & DOCUMENTATION
-- --------------------------
COMMENT ON TABLE public.[TABLE_NAME] IS '[COMPREHENSIVE_TABLE_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';
COMMENT ON COLUMN public.[TABLE_NAME].[FIELD_NAME] IS '[DETAILED_FIELD_DESCRIPTION]';

-- 6. RELATIONSHIPS
-- --------------
/*
  This table has the following relationships with other tables:

  - [RELATIONSHIP_1]: [DESCRIBE_RELATIONSHIP_1]
  - [RELATIONSHIP_2]: [DESCRIBE_RELATIONSHIP_2]
  - [RELATIONSHIP_3]: [DESCRIBE_RELATIONSHIP_3]
*/

-- 7. QUERY PATTERNS
-- ---------------
/*
  Common query patterns for this table:

  1. [QUERY_PATTERN_1]:
     ```sql
     [SQL_QUERY_EXAMPLE_1]
     ```

  2. [QUERY_PATTERN_2]:
     ```sql
     [SQL_QUERY_EXAMPLE_2]
     ```

  3. [QUERY_PATTERN_3]:
     ```sql
     [SQL_QUERY_EXAMPLE_3]
     ```
*/

-- 8. PERFORMANCE CONSIDERATIONS
-- ---------------------------
/*
  - [PERFORMANCE_CONSIDERATION_1]
  - [PERFORMANCE_CONSIDERATION_2]
  - [PERFORMANCE_CONSIDERATION_3]
*/

-- 9. SECURITY & ACCESS CONTROL
-- --------------------------
/*
  - [SECURITY_CONSIDERATION_1]
  - [SECURITY_CONSIDERATION_2]
  - [SECURITY_CONSIDERATION_3]
*/

-- 10. EVOLUTION & FUTURE CONSIDERATIONS
-- -----------------------------------
/*
  Planned enhancements:
  - [PLANNED_ENHANCEMENT_1]
  - [PLANNED_ENHANCEMENT_2]
  - [PLANNED_ENHANCEMENT_3]

  Potential extensions:
  - [POTENTIAL_EXTENSION_1]
  - [POTENTIAL_EXTENSION_2]
  - [POTENTIAL_EXTENSION_3]
*/

-- 11. CHANGE HISTORY
-- ----------------
/*
  | Version | Date       | Author        | Description                  |
  |---------|------------|---------------|------------------------------|
  | [V1]    | [DATE_1]   | [AUTHOR_1]    | [DESCRIPTION_1]              |
  | [V2]    | [DATE_2]   | [AUTHOR_2]    | [DESCRIPTION_2]              |
  | [V3]    | [DATE_3]   | [AUTHOR_3]    | [DESCRIPTION_3]              |
*/

-- =========================================================================
-- SIMPLE EXAMPLE: users
-- =========================================================================
/*
  OVERVIEW
  --------
  Stores global user data used by all applications in the ecosystem.
  
  This table maintains core user profile information, authentication details, and global preferences
  that persist across all platforms (Grasshop, Tribes, Should I Launch).
  
  The user record serves as the central identity reference point, with other tables linking
  to users via the id field.
*/

-- 1. DESIGN PRINCIPLES & PHILOSOPHY
-- --------------------------------
/*
  This table design is guided by the following principles:

  1. Single Source of Truth: User identity is maintained in one central location
  2. Extensibility: The profile JSONB field allows for expansion without schema changes
  3. Minimal Core Fields: Only essential fields are stored as columns, with extensions in JSONB
  
  These principles align with the system's broader architectural goals of flexibility and scalability.
*/

-- 2. KEY DESIGN DECISIONS
-- ----------------------
/*
  1. TEXT for ID: Using TEXT type for IDs to support various ID formats from auth providers
  2. JSONB for Profile: Using JSONB for extensible profile data rather than multiple columns
  3. Unique Constraints: Enforcing uniqueness on both username and email
*/

-- 3. SCHEMA DEFINITION
-- -------------------
CREATE TABLE public.users (
  id TEXT PRIMARY KEY,                        -- Unique internal user ID
  username TEXT UNIQUE NOT NULL,              -- Public username for display/mentions
  email TEXT UNIQUE NOT NULL,                 -- User's login email address
  profile JSONB NOT NULL DEFAULT '{
    "bio": null,                              -- User's self-description 
    "social": {                               -- Collection of social media links
      "twitter": null,                        -- Twitter/X username or URL
      "github": null                          -- GitHub username or URL
    }
  }'::jsonb,                                  -- Extended profile information
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- Account creation timestamp
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  -- Last update timestamp
);

-- 4. INDEXES & CONSTRAINTS
-- -----------------------
-- Indexes
CREATE INDEX idx_users_username ON public.users(username);
CREATE INDEX idx_users_email ON public.users(email);

-- 5. COMMENTS & DOCUMENTATION
-- --------------------------
COMMENT ON TABLE public.users IS 'Stores global user data used by all applications in the ecosystem';
COMMENT ON COLUMN public.users.id IS 'Unique identifier for the user';
COMMENT ON COLUMN public.users.username IS 'Public username for display and @mentions';
COMMENT ON COLUMN public.users.email IS 'User''s primary email address for login and notifications';
COMMENT ON COLUMN public.users.profile IS 'Extended profile information including bio and social links';
COMMENT ON COLUMN public.users.created_at IS 'Timestamp when the user account was created';
COMMENT ON COLUMN public.users.updated_at IS 'Timestamp when the user record was last modified';

-- 6. RELATIONSHIPS
-- --------------
/*
  This table has the following relationships with other tables:

  - One-to-Many with user_preferences: Each user can have multiple preference records
  - One-to-Many with content_items: Each user can create multiple content items
  - One-to-Many with user_connections: Each user can have multiple connections to other users
*/

-- 7. QUERY PATTERNS
-- ---------------
/*
  Common query patterns for this table:

  1. User lookup by username:
     ```sql
     SELECT * FROM public.users WHERE username = 'example_user';
     ```

  2. User profile retrieval with specific JSONB fields:
     ```sql
     SELECT id, username, profile->>'bio' AS bio, 
            profile->'social'->>'twitter' AS twitter 
     FROM public.users WHERE id = 'user_id';
     ```

  3. Finding users with specific profile attributes:
     ```sql
     SELECT * FROM public.users 
     WHERE profile->'social'->>'twitter' IS NOT NULL;
     ```
*/

-- 8. PERFORMANCE CONSIDERATIONS
-- ---------------------------
/*
  - Username and email lookups are common, so indexes are created for both
  - Consider adding GIN indexes on profile JSONB if querying specific profile attributes becomes common
  - Monitor query performance on large user tables and consider partitioning if necessary
*/

-- 9. SECURITY & ACCESS CONTROL
-- --------------------------
/*
  - Email addresses should be protected and not exposed in public APIs
  - Consider encrypting sensitive profile data
  - Implement row-level security policies to control access to user records
*/

-- 10. EVOLUTION & FUTURE CONSIDERATIONS
-- -----------------------------------
/*
  Planned enhancements:
  - Add support for multiple email addresses per user
  - Implement more granular privacy controls for profile fields
  - Add verification status for social media links

  Potential extensions:
  - Integration with external identity providers
  - Support for user groups and organizational accounts
  - Enhanced analytics on user engagement patterns
*/

-- 11. CHANGE HISTORY
-- ----------------
/*
  | Version | Date         | Author          | Description                           |
  |---------|--------------|-----------------|---------------------------------------|
  | 1.0     | 2023-01-15   | Jane Developer  | Initial schema creation               |
  | 1.1     | 2023-03-22   | John Architect  | Added social links to profile JSONB   |
  | 1.2     | 2023-06-10   | Alex Engineer   | Added indexes for performance         |
*/

-- =========================================================================
-- MEDIUM EXAMPLE: actions
-- =========================================================================
/*
  OVERVIEW
  --------
  Stores gamification and engagement elements like challenges, tournaments, and events.
  
  This table defines structured activities that users can participate in, with flexible 
  configuration options through JSONB fields to support different action types without
  requiring schema changes.
  
  Actions can be attached to communities, tribes, or other entities through the reference_type
  and reference_id fields, enabling contextual activities within different spaces.
*/

-- 1. DESIGN PRINCIPLES & PHILOSOPHY
-- --------------------------------
/*
  This table design is guided by the following principles:

  1. Flexibility: Supporting multiple action types with a single schema
  2. Contextual Relevance: Actions can be associated with different entity types
  3. Configurability: Extensive use of JSONB for type-specific configurations
  
  These principles align with the system's broader architectural goals of adaptability and extensibility.
*/

-- 2. KEY DESIGN DECISIONS
-- ----------------------
/*
  1. Reference Fields: Using reference_type and reference_id for polymorphic associations
  2. Multiple JSONB Fields: Separating different aspects (config, requirements, rewards) into distinct JSONB fields
  3. Status Field: Explicit status field for lifecycle management
*/

-- 3. SCHEMA DEFINITION
-- -------------------
CREATE TABLE public.actions (
  id TEXT PRIMARY KEY,                        -- Unique identifier for this action
  name TEXT NOT NULL,                         -- Display name of the action
  description TEXT,                           -- Detailed explanation of what this action entails
  action_type TEXT NOT NULL,                  -- "challenge", "tournament", "season", "event", etc.
  status TEXT NOT NULL DEFAULT 'draft',       -- "draft", "active", "completed", "cancelled", "archived"
  reference_type TEXT NOT NULL,               -- Entity type this action is associated with
  reference_id TEXT NOT NULL,                 -- ID of the entity this action is associated with
  creator_id TEXT NOT NULL,                   -- User who created this action
  visibility TEXT NOT NULL DEFAULT 'members', -- "public", "members", "invited", "private"
  config JSONB NOT NULL DEFAULT '{
    "difficulty": "normal",                   -- Difficulty level of this action
    "type_specific": {},                      -- Configuration specific to the action type
    "display": {                              -- Visual display configuration
      "color": null,                          -- Custom color for UI elements
      "icon": null,                           -- Icon identifier for this action
      "header_image": null                    -- URL for header image
    }
  }'::jsonb,                                  -- Type-specific configuration settings
  requirements JSONB NOT NULL DEFAULT '{
    "prerequisites": [],                      -- Actions or achievements required before participation
    "constraints": {},                        -- Limiting factors for participation
    "success_criteria": {}                    -- Conditions for completing the action
  }'::jsonb,                                  -- Participation and completion requirements
  rewards_config JSONB NOT NULL DEFAULT '{
    "instant": [],                            -- Rewards given immediately upon completion
    "milestone": [],                          -- Rewards given at specific progress points
    "random": [],                             -- Chance-based rewards with probability settings
    "conditional": []                         -- Rewards with special requirements
  }'::jsonb,                                  -- Rewards associated with this action
  schedule JSONB NOT NULL DEFAULT '{
    "starts_at": null,                        -- When this action becomes available
    "ends_at": null,                          -- When this action concludes
    "duration": null,                         -- How long the action lasts
    "recurring": false                        -- Whether this repeats on a schedule
  }'::jsonb,                                  -- Timing parameters
  metadata JSONB NOT NULL DEFAULT '{
    "tags": [],                               -- Categorization tags
    "ai_generated": false,                    -- Whether created by AI
    "template_id": null                       -- Reference to template if created from one
  }'::jsonb,                                  -- Additional action details
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. INDEXES & CONSTRAINTS
-- -----------------------
-- Indexes
CREATE INDEX idx_actions_type ON public.actions(action_type);
CREATE INDEX idx_actions_status ON public.actions(status);
CREATE INDEX idx_actions_reference ON public.actions(reference_type, reference_id);
CREATE INDEX idx_actions_creator ON public.actions(creator_id);
CREATE INDEX idx_actions_schedule ON public.actions((schedule->>'starts_at'), (schedule->>'ends_at'));

-- 5. COMMENTS & DOCUMENTATION
-- --------------------------
COMMENT ON TABLE public.actions IS 'Stores gamification and engagement elements like challenges, tournaments, and events';
COMMENT ON COLUMN public.actions.id IS 'Unique identifier for this action';
COMMENT ON COLUMN public.actions.name IS 'Display name of the action shown to users';
COMMENT ON COLUMN public.actions.description IS 'Detailed explanation of what this action entails';
COMMENT ON COLUMN public.actions.action_type IS 'Categorization like "challenge", "tournament", "season", or "event"';
COMMENT ON COLUMN public.actions.status IS 'Current state of the action (draft, active, completed, etc.)';
COMMENT ON COLUMN public.actions.reference_type IS 'Entity type this action is associated with (community, tribe, etc.)';
COMMENT ON COLUMN public.actions.reference_id IS 'ID of the entity this action is associated with';
COMMENT ON COLUMN public.actions.creator_id IS 'User who created this action';
COMMENT ON COLUMN public.actions.visibility IS 'Who can see this action (public, members, invited, etc.)';
COMMENT ON COLUMN public.actions.config IS 'Comprehensive JSONB configuration with type-specific settings';
COMMENT ON COLUMN public.actions.requirements IS 'Conditions for participation or completion';
COMMENT ON COLUMN public.actions.rewards_config IS 'Definition of rewards earned through this action';
COMMENT ON COLUMN public.actions.schedule IS 'Timing parameters for the action';
COMMENT ON COLUMN public.actions.metadata IS 'Additional action details and administrative data';
COMMENT ON COLUMN public.actions.created_at IS 'Timestamp when the action was created';
COMMENT ON COLUMN public.actions.updated_at IS 'Timestamp when the action was last modified';

-- 6. RELATIONSHIPS
-- --------------
/*
  This table has the following relationships with other tables:

  - Many-to-One with users: Each action has a creator (creator_id)
  - One-to-Many with action_participants: Each action can have multiple participants
  - One-to-Many with action_submissions: Each action can have multiple submissions
  - Polymorphic association with various entities via reference_type and reference_id
*/

-- 7. QUERY PATTERNS
-- ---------------
/*
  Common query patterns for this table:

  1. Finding active actions for a specific context:
     ```sql
     SELECT * FROM public.actions 
     WHERE reference_type = 'community' AND reference_id = 'community_id'
     AND status = 'active';
     ```

  2. Finding upcoming actions:
     ```sql
     SELECT * FROM public.actions 
     WHERE (schedule->>'starts_at')::timestamptz > NOW()
     ORDER BY (schedule->>'starts_at')::timestamptz ASC;
     ```

  3. Finding actions with specific tags:
     ```sql
     SELECT * FROM public.actions 
     WHERE metadata->'tags' ? 'featured';
     ```
*/

-- 8. PERFORMANCE CONSIDERATIONS
-- ---------------------------
/*
  - Composite index on reference_type and reference_id for efficient lookups
  - Index on schedule fields for time-based queries
  - Consider GIN indexes for JSONB fields if querying specific JSONB properties becomes common
  - Monitor query performance on large action tables and consider partitioning by action_type if necessary
*/

-- 9. SECURITY & ACCESS CONTROL
-- --------------------------
/*
  - Implement visibility checks in application code based on the visibility field
  - Ensure creator_id references are validated against authenticated users
  - Consider row-level security policies for fine-grained access control
*/

-- 10. EVOLUTION & FUTURE CONSIDERATIONS
-- -----------------------------------
/*
  Planned enhancements:
  - Support for team-based actions
  - Enhanced scheduling options for recurring actions
  - More sophisticated reward distribution mechanisms

  Potential extensions:
  - Integration with notification systems
  - AI-driven action recommendations
  - Analytics dashboard for action engagement metrics
*/

-- 11. CHANGE HISTORY
-- ----------------
/*
  | Version | Date         | Author          | Description                           |
  |---------|--------------|-----------------|---------------------------------------|
  | 1.0     | 2023-02-20   | Sam Designer    | Initial schema creation               |
  | 1.1     | 2023-04-15   | Taylor Dev      | Added metadata field                  |
  | 1.2     | 2023-07-05   | Jordan Architect| Enhanced reward configuration options |
*/

-- =========================================================================
-- COMPLEX EXAMPLE: permission_templates
-- =========================================================================
/*
  OVERVIEW
  --------
  Defines reusable permission configurations that can be applied to users in various contexts.
  
  This table stores comprehensive permission blueprints that define granular access controls
  across the entire platform. Each template contains a detailed JSONB structure that outlines
  what actions are allowed on different entity types, with attribute-level control and 
  conditional rules.
  
  Permission templates serve as the foundation of the access control system, providing a
  hierarchical permission model where specific permissions can inherit from and override
  these baseline configurations.
*/

-- 1. DESIGN PRINCIPLES & PHILOSOPHY
-- --------------------------------
/*
  This table design is guided by the following principles:

  1. Reusability: Templates can be applied across multiple contexts
  2. Granularity: Permissions can be defined at various levels of specificity
  3. Hierarchical Structure: Permissions follow an inheritance model
  
  These principles align with the system's broader architectural goals of flexibility and security.
*/

-- 2. KEY DESIGN DECISIONS
-- ----------------------
/*
  1. Complex JSONB Structure: Using a deeply nested JSONB structure for comprehensive permission definition
  2. Metadata Separation: Keeping administrative metadata separate from the permission configuration
  3. Minimal Schema: Using a simple table structure with complex JSONB fields rather than multiple related tables
*/

-- 3. SCHEMA DEFINITION
-- -------------------
CREATE TABLE public.permission_templates (
  id TEXT PRIMARY KEY,                        -- Unique identifier for the permission template
  name TEXT NOT NULL,                         -- Human-readable name (e.g., "Content Moderator")
  default_permissions JSONB NOT NULL DEFAULT '{
    "global_settings": {                      -- System-wide configurations for all permissions
      "default_access": "read",               -- Base permission when no other rules apply
      "time_windows": [],                     -- Time periods when permissions are active
      "usage_quotas": {}                      -- Limits on frequency/quantity of actions
    },
    "entity_type_permissions": {              -- Permissions organized by entity type
      "dots": {                               -- Rules for content items
        "create": true,                       -- Whether user can create new dots
        "edit": {                             -- Rules for editing dots
          "allowed": true,                    -- Base permission to edit dots
          "attributes": ["title", "content"], -- Which dot fields can be edited
          "conditions": {}                    -- Requirements to allow editing
        },
        "delete": false                       -- Whether user can delete dots
      },
      "tags": {                               -- Rules for tag entities
        "create": true,                       -- Whether user can create tags
        "edit": {                             -- Rules for editing tags
          "allowed": false,                   -- Base permission to edit tags
          "system_tags": false,               -- Whether user can edit system tags
          "user_tags": true                   -- Whether user can edit user tags
        },
        "delete": false                       -- Whether user can delete tags
      }
    },
    "tag_based_permissions": {                -- Permissions based on content tags
      "draft": {                              -- Rules for items tagged as "draft"
        "edit": true,                         -- Whether user can edit draft items
        "delete": false,                      -- Whether user can delete draft items
        "applies_to": ["dots", "actions"]     -- Entity types affected by this rule
      }
    },
    "relationship_based_permissions": {},     -- Permissions based on entity relationships
    "membership_based_permissions": {},       -- Permissions based on member status/tenure
    "api_permissions": {                      -- Rules for API access
      "access": false,                        -- Whether user can access APIs
      "endpoints": []                         -- Which endpoints user can access
    }
  }'::jsonb,                                  -- Hierarchical permission configuration
  metadata JSONB NOT NULL DEFAULT '{
    "created_by": null,                       -- User ID of template creator
    "description": null,                      -- Detailed description of template purpose
    "version": 1,                             -- Template version number
    "is_system": false,                       -- Whether this is a system-defined template
    "applicable_contexts": ["community", "tribe", "action"] -- Where template can be applied
  }'::jsonb,                                  -- Administrative metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW() -- Creation timestamp
);

-- 4. INDEXES & CONSTRAINTS
-- -----------------------
-- Indexes
CREATE INDEX idx_permission_templates_name ON public.permission_templates(name);
CREATE INDEX idx_permission_templates_system ON public.permission_templates((metadata->>'is_system'));

-- 5. COMMENTS & DOCUMENTATION
-- --------------------------
COMMENT ON TABLE public.permission_templates IS 'Defines reusable permission configurations that can be applied to users in various contexts';
COMMENT ON COLUMN public.permission_templates.id IS 'Unique identifier for the permission template';
COMMENT ON COLUMN public.permission_templates.name IS 'Human-readable name for the template (e.g., "Content Moderator", "Community Admin")';
COMMENT ON COLUMN public.permission_templates.default_permissions IS 'JSONB structure containing hierarchical permission configuration including global settings, entity-type permissions, and tag-based permissions';
COMMENT ON COLUMN public.permission_templates.metadata IS 'Administrative metadata about the template (creator, description, version)';
COMMENT ON COLUMN public.permission_templates.created_at IS 'Timestamp when the template was created';

-- 6. RELATIONSHIPS
-- --------------
/*
  This table has the following relationships with other tables:

  - One-to-Many with user_permissions: Each template can be applied to multiple users
  - Many-to-One with users: Each template has a creator (metadata->>'created_by')
  - Referenced by various context-specific permission tables
*/

-- 7. QUERY PATTERNS
-- ---------------
/*
  Common query patterns for this table:

  1. Finding system-defined templates:
     ```sql
     SELECT * FROM public.permission_templates 
     WHERE metadata->>'is_system' = 'true';
     ```

  2. Finding templates applicable to a specific context:
     ```sql
     SELECT * FROM public.permission_templates 
     WHERE metadata->'applicable_contexts' ? 'community';
     ```

  3. Finding templates with specific permissions:
     ```sql
     SELECT * FROM public.permission_templates 
     WHERE default_permissions->'entity_type_permissions'->'dots'->>'create' = 'true';
     ```
*/

-- 8. PERFORMANCE CONSIDERATIONS
-- ---------------------------
/*
  - Index on is_system for efficient filtering of system vs. custom templates
  - Consider GIN indexes for complex JSONB queries if they become common
  - The JSONB structure is complex, so monitor query performance and optimize as needed
*/

-- 9. SECURITY & ACCESS CONTROL
-- --------------------------
/*
  - Restrict template creation and modification to administrative users
  - Validate permission structures against a schema to prevent invalid configurations
  - Consider versioning and audit trails for permission changes
*/

-- 10. EVOLUTION & FUTURE CONSIDERATIONS
-- -----------------------------------
/*
  Planned enhancements:
  - Support for conditional permissions based on user attributes
  - Enhanced time-based permission controls
  - Permission inheritance and override mechanisms

  Potential extensions:
  - Integration with external identity providers
  - Permission analytics and visualization tools
  - AI-assisted permission recommendations
*/

-- 11. CHANGE HISTORY
-- ----------------
/*
  | Version | Date         | Author          | Description                           |
  |---------|--------------|-----------------|---------------------------------------|
  | 1.0     | 2023-03-10   | Riley Security  | Initial schema creation               |
  | 1.1     | 2023-05-20   | Casey Admin     | Added tag-based permissions           |
  | 1.2     | 2023-08-15   | Morgan Architect| Enhanced API permission controls      |
*/
